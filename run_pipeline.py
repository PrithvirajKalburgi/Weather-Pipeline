import luigi
from config import CITIES
from luigi_pipeline.merge_and_average import MergeandAverageData

if __name__ == '__main__':
    for city in CITIES:
        luigi.build([MergeandAverageData(city=city)], local_scheduler = True)