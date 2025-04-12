import luigi
import sqlite3
import json
import time
from luigi import LocalTarget
from luigi_pipeline.fetch_openweather import FetchOpenWeatherData
from luigi_pipeline.fetch_weatherapi import FetchWeatherAPIData
from config import DB_PATH

class StoreRawData(luigi.Task):
    city = luigi.Parameter()

    def requires(self):
        return [FetchOpenWeatherData(city=self.city), FetchWeatherAPIData(city=self.city)]
    
    def output(self):
        return luigi.LocalTarget(f'data/store_{self.city}_raw_data.db')
    
    def run(self):
        DB_PATH = self.output().path
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Create the table with the timestamp column
        cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS weather_data (
           city TEXT,
           source TEXT,
           temperature REAL,
           wind_speed REAL,
           humidity REAL,
           feels_like REAL,
           timestamp TEXT
        )
        ''')

        with self.input()[0].open('r') as f:
            openweather_data = json.load(f)

        with self.input()[1].open('r') as f:
            weatherapi_data = json.load(f)

        # Assuming we want to use the localtime from WeatherAPI as timestamp
        timestamp = weatherapi_data['location']['localtime']

        # Insert data from OpenWeather
        cursor.execute('''
        INSERT INTO weather_data (city, source, temperature, wind_speed, humidity, feels_like, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (self.city, 'openweather', 
              openweather_data['main']['temp'],
              openweather_data['wind']['speed'], 
              openweather_data['main']['humidity'],
              openweather_data['main']['feels_like'],
              timestamp
              ))

        # Insert data from WeatherAPI
        cursor.execute('''
        INSERT INTO weather_data (city, source, temperature, wind_speed, humidity, feels_like, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (self.city, 'weatherapi', 
              weatherapi_data['current']['temp_c'],
              weatherapi_data['current']['wind_kph'], 
              weatherapi_data['current']['humidity'],
              weatherapi_data['current']['feelslike_c'],
              timestamp
              ))

        conn.commit()
        conn.close()

    