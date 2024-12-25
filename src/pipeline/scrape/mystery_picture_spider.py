import json

import scrapy
from typing import Any, Dict, Iterable
from bs4 import BeautifulSoup
from scrapy.http import Request, Response
from scrapy import Field, Item

from settings import USER_AGENT, KAFKA_TOPIC_MYSTERY_PICTURE


class MysteryPictureAPIItem(Item):
    api_response = Field()


class MysteryPictureSpider(scrapy.Spider):
    name = "mystery-picture-spider"
    custom_settings = {"KAFKA_TOPIC": KAFKA_TOPIC_MYSTERY_PICTURE}
    batch_size = 50

    def start_requests(self) -> Iterable[Request]:
        # ! TODO !
        # Change this function to scrape the Mystery Picture API.
        raise NotImplemented


    def parse(self, response: Response, **kwargs: Any) -> Any:
        # ! TODO !
        # Change this function to scrape the Mystery Picture API.
        raise NotImplemented
