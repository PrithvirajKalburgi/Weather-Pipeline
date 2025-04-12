import luigi
import sqlite3
import pandas as pd
import json
from luigi import LocalTarget
from luigi_pipeline.store_raw_data import StoreRawData
from config import DB_PATH

class MergeandAverageData(luigi.Task):
    city = luigi.Parameter()

    def requires(self):
        return StoreRawData(city=self.city)
    
    def output(self):
        return LocalTarget(f'data/merged_and_averaged_{self.city}.json')
    
    def run(self):
        conn = sqlite3.connect(DB_PATH)
        query = "SELECT * FROM weather_data WHERE city = ?"
        df = pd.read_sql(query, conn, params=(self.city,))

        avg_data = {
            'temperature': df['temperature'].mean(),
            'wind_speed': df['wind_speed']. mean(),
            'humidity': df['humidity'].mean(),
            'feels_like': df['feels_like'].mean()
        }

        with self.output().open('w') as f:
            json.dump(avg_data, f)

        conn.close()

