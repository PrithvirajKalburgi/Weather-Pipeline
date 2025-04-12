import luigi
import requests
import json
from config import WEATHERAPI_API_KEY, CITIES

class FetchWeatherAPIData(luigi.Task):
    city = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget(f'data/weatherapi_{self.city}.json')
    
    def run(self):
        url = f'http://api.weatherapi.com/v1/current.json?key={WEATHERAPI_API_KEY}&q={self.city}&aqi=no'

        response = requests.get(url)
        data = response.json()
        
        with self.output().open('w') as f:
            json.dump(data, f)