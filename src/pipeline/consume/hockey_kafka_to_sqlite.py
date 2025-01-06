from confluent_kafka import Consumer, KafkaError
import json
from bs4 import BeautifulSoup
from typing import List

from settings import KAFKA_CONFIGS, KAFKA_TOPIC_HOCKEY_RESULTS
from common.hockey import HockeyTeamResults, HockeyTeamResultsDict


def ele_has_class(ele, cls: str) -> bool:
    if ele.attrs:
        classes = ele.attrs.get("class")
        if classes and cls in classes:
            return True
        return False


def parse_table(table: BeautifulSoup) -> List[HockeyTeamResultsDict]:
    headers = [" ".join(x.get_text(separator=' ').split()) for x in table.find_all("th")]
    rows = []
    formatted_rows = []
    for row in table.find_all("tr"):
        if ele_has_class(row, "total_row"):
            continue
        row_values = row.find_all("td")
        if len(row_values) > 0:
            rows.append(x.text.strip() for x in row_values)
    teams = [dict(zip(headers, row)) for row in rows]

    for team in teams:
        formatted_rows.append(HockeyTeamResultsDict(
            TeamName=team["Team Name"],
            Year=team["Year"],
            Wins=team["Wins"],
            Losses=team["Losses"],
            OTLosses=team["OT Losses"] if team["OT Losses"] != '' else None,
            WinPct=team["Win %"],
            GoalsFor=team["Goals For (GF)"],
            GoalsAgainst=team["Goals Against (GA)"],
            GoalsDifference=team["+ / -"],
        ))

    return formatted_rows


def hockey_push_to_sqlite():
    consumer = Consumer({
        "bootstrap.servers": KAFKA_CONFIGS["bootstrap.servers"],
        "group.id": "sqlite",
        "auto.offset.reset": "earliest"
    })

    def print_assignment(consumer, partitions):
        print('Assignment', partitions)

    consumer.subscribe([KAFKA_TOPIC_HOCKEY_RESULTS], on_assign=print_assignment)
    hockey_team_results = HockeyTeamResults()

    while True:
        msg = consumer.poll(10.0)

        if msg is None:
            print("no more messages")
            # No more messages
            break
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break
        consumed_data = json.loads(msg.value().decode("utf-8"))
        body = BeautifulSoup(consumed_data["body"], "lxml")
        hockey_table = body.find("table")
        if not hockey_table:
            raise ValueError("No table can be found")

        formatted_rows: List[HockeyTeamResultsDict] = parse_table(hockey_table)
        hockey_team_results.insert_data(formatted_rows)

    consumer.close()
