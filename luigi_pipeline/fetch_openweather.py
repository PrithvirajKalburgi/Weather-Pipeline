import luigi
import requests
import json
from config import OPENWEATHER_API_KEY, CITIES

class FetchOpenWeatherData(luigi.Task):
    city = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget(f'data/openweather_{self.city}.json')
    
    def run(self):
        url = f'http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={OPENWEATHER_API_KEY}&units=metric'

        response = requests.get(url)
        data = response.json()

        with self.output().open('w') as f:
            json.dump(data, f)

            