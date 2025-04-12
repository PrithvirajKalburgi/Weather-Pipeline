import luigi
from config import CITIES
from luigi_pipeline.merge_and_average import MergeandAverageData
from luigi_pipeline.visualise import visualise_weather_data

if __name__ == '__main__':
    for city in CITIES:
        luigi.build([MergeandAverageData(city=city)], local_scheduler = True)

    visualise_weather_data(CITIES)