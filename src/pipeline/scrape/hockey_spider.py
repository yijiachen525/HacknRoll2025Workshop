import scrapy
from typing import Any, Iterable
from scrapy.http import Request, Response
from scrapy import Field, Item

from settings import USER_AGENT, KAFKA_TOPIC_HOCKEY_RESULTS


class HockeyResultsItem(Item):
    body = Field()


class HockeyResultsSpider(scrapy.Spider):
    name = "hockey-results-spider"
    custom_settings = {"KAFKA_TOPIC": KAFKA_TOPIC_HOCKEY_RESULTS}

    def start_requests(self) -> Iterable[Request]:
        # Initial request(s): scrape the first page
        yield Request(
            url="https://www.scrapethissite.com/pages/forms/?per_page=15",
            headers={"User-Agent": USER_AGENT},
            meta={"page": 1}  # pass an initial page number of 1 in the metadata
        )

    def parse(self, response: Response, **kwargs: Any) -> Any:
        # yield a HockeyResultsItem, which is what will be inserted to Kafka
        # The HockeyResultsItem just contains a `body` field which is the raw HTML from the page.
        yield HockeyResultsItem(body=str(response.text))

        # Derive the next page from the request's metadata
        next_page = int(response.meta["page"]) + 1
        if f"?page_num={next_page}" in response.text:
            # if (what looks like) the link to the webpage is in the response HTML, we're not on the last page,
            # so yield another Request to scrape the next page
            yield Request(
                url=f"https://www.scrapethissite.com/pages/forms/?page_num={next_page}&per_page=15",
                headers={"User-Agent": USER_AGENT},
                meta={"page": next_page}
            )
