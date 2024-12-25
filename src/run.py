from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
import os

from common.hockey import HockeyTeamResults
from common.mystery_picture import MysteryPicture
from pipeline.consume.hockey_kafka_to_sqlite import hockey_push_to_sqlite
from pipeline.consume.mystery_picture_to_sqlite import mystery_picture_push_to_sqlite
from pipeline.scrape.mystery_picture_spider import MysteryPictureSpider
from pipeline.util import ensure_kafka_connectivity
from settings import KAFKA_CONFIGS
from pipeline.scrape.hockey_spider import HockeyResultsSpider

if __name__ == "__main__":
    settings = Settings()
    os.environ["SCRAPY_SETTINGS_MODULE"] = "settings"
    ensure_kafka_connectivity(KAFKA_CONFIGS)
    settings_module_path = os.environ["SCRAPY_SETTINGS_MODULE"]
    settings.setmodule(settings_module_path, priority="project")
    process = CrawlerProcess(settings)

    # task 1
    process.crawl(HockeyResultsSpider)
    print("Start Crawling")
    process.start()
    print("Create table")
    HockeyTeamResults().create_table()
    print("Start inserting")
    hockey_push_to_sqlite()

    ## task 2
    # process.crawl(MysteryPictureSpider)
    # MysteryPicture().create_table()
    # print("Start Crawling")
    # process.start()
    # print("Start inserting")
    # mystery_picture_push_to_sqlite()
