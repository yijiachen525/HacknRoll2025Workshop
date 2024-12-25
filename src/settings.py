from pathlib import Path

SQLITE_DATABASE = "HacknRoll2025"
SQLITE_TABLE_HOCKEY_RESULTS = "HockeyTeamResults"
SQLITE_TABLE_MYSTERY_PICTURE = "MysteryPicture"
DB_PATH = str((Path(__file__).parent.parent / "db").absolute())
KAFKA_CONFIGS = {"bootstrap.servers": "localhost:9093"}
KAFKA_TOPIC_HOCKEY_RESULTS = "hockey-team-results"
KAFKA_TOPIC_MYSTERY_PICTURE = "mystery-picture"


# for scrapy
USER_AGENT = "Python/3. Scrapy/2.11"
DOWNLOAD_DELAY = 0.1  # 1 second in between requests
SPIDER_MODULES = ["pipeline.scrape"]
ITEM_PIPELINES = {"pipeline.scrape.kafka_pipeline.KafkaPipeline": 0}
