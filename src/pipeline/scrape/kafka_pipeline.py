from datetime import datetime

from confluent_kafka.admin import AdminClient
from itemadapter import ItemAdapter
from confluent_kafka import Producer, KafkaError, Message
from scrapy import Spider, Item
from scrapy.crawler import Crawler
from typing import Type, TypeVar
import json

T = TypeVar("T", bound=Item)


class KafkaPipeline:
    def __init__(self, kafka_configs: dict, topic: str) -> None:
        self.producer = Producer(**kafka_configs)
        self.topic = topic
        self.kafka_configs = kafka_configs

    @classmethod
    def from_crawler(cls: Type["KafkaPipeline"], crawler: Crawler) -> "KafkaPipeline":
        return cls(
            kafka_configs=crawler.settings.get("KAFKA_CONFIGS"),
            topic=crawler.settings.get("KAFKA_TOPIC"),
        )

    def open_spider(self, spider: Spider) -> None:
        print("open spider")

    def close_spider(self, spider: Spider) -> None:
        print("close")
        self.producer.flush()

    def process_item(self, item: T, spider: Spider) -> T:
        print("process item")
        self.producer.produce(self.topic, json.dumps(ItemAdapter(item).asdict()), on_delivery=self._delivery_report)
        self.producer.poll(0)
        return item

    def _delivery_report(self, err: KafkaError, msg: Message) -> None:
        if err is not None:
            print(f"Delivery failed for record at offset {msg.offset()}: {err}")
            return
        print(f"User record successfully produced to {msg.topic()} at offset {msg.offset()}")
