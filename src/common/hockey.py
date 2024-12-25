import sqlite3
from cachetools.func import ttl_cache
from itertools import chain
from enum import Enum
from typing import TypedDict, Optional, List

from settings import SQLITE_DATABASE, SQLITE_TABLE_HOCKEY_RESULTS, DB_PATH

SQLITE_MAX_ARGS = 100

class HockeyTeamResultsDict(TypedDict):
    TeamName: str
    Year: int
    Wins: int
    Losses: int
    OTLosses: Optional[int]
    WinPct: float
    GoalsFor: int
    GoalsAgainst: int
    GoalsDifference: int


class HockeyTeamResults:
    def create_table(self):
        conn = sqlite3.connect(f"{DB_PATH}/{SQLITE_DATABASE}.db")
        conn.execute(f"""
            DROP TABLE IF EXISTS {SQLITE_TABLE_HOCKEY_RESULTS}
        """)
        conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {SQLITE_TABLE_HOCKEY_RESULTS} (
                TeamName TEXT NOT NULL,
                Year INT NOT NULL,
                Wins INT NOT NULL,
                Losses INT NOT NULL,
                OTLosses INT NULL,
                WinPct FLOAT NOT NULL,
                GoalsFor INT NOT NULL,
                GoalsAgainst INT NOT NULL,
                GoalsDifference INT NOT NULL,
                LastUpdateDateUtc DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

                PRIMARY KEY(TeamName, Year)
            )
        """)
        conn.close()

    def insert_data(self, data: List[HockeyTeamResultsDict]) -> None:
        if len(data) > 0:
            args_per_item = len(data[0])
            batch_size = SQLITE_MAX_ARGS // args_per_item
            print("into db")

            conn = sqlite3.connect(f"{DB_PATH}/{SQLITE_DATABASE}.db")
            conn.execute("BEGIN TRANSACTION")
            for i in range(0, len(data), batch_size):
                data_to_insert = data[i:i+batch_size]
                params = [
                    (
                        item["TeamName"],
                        item["Year"],
                        item["Wins"],
                        item["Losses"],
                        item["OTLosses"],
                        item["WinPct"],
                        item["GoalsFor"],
                        item["GoalsAgainst"],
                        item["GoalsDifference"],
                    )
                    for item in data_to_insert
                ]
                print(params)

                conn.executemany(f"""
                    INSERT OR REPLACE INTO {SQLITE_TABLE_HOCKEY_RESULTS} (
                        TeamName,
                        Year,
                        Wins,
                        Losses,
                        OTLosses,
                        WinPct,
                        GoalsFor,
                        GoalsAgainst,
                        GoalsDifference
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, params)
            conn.commit()
            conn.close()


    @ttl_cache(maxsize=1, ttl=5)
    def get_data(self) -> List[HockeyTeamResultsDict]:
        conn = sqlite3.connect(f"{DB_PATH}/{SQLITE_DATABASE}.db")
        data = conn.execute(f"""
            SELECT
                TeamName,
                Year,
                Wins,
                Losses,
                OTLosses,
                WinPct,
                GoalsFor,
                GoalsAgainst,
                GoalsDifference
            FROM {SQLITE_TABLE_HOCKEY_RESULTS}
        """).fetchall()
        conn.close()
        return [
            HockeyTeamResultsDict(
                TeamName=item[0],
                Year=item[1],
                Wins=item[2],
                Losses=item[3],
                OTLosses=item[4],
                WinPct=item[5],
                GoalsFor=item[6],
                GoalsAgainst=item[7],
                GoalsDifference=item[8],
            )
            for item in data
        ]
    
    @ttl_cache(maxsize=1, ttl=5)
    def get_all_data(self) -> List[HockeyTeamResultsDict]:
        conn = sqlite3.connect(f"{DB_PATH}/{SQLITE_DATABASE}.db")
        data = conn.execute(f"""
            SELECT
                TeamName,
                Year,
                Wins,
                Losses,
                OTLosses,
                WinPct,
                GoalsFor,
                GoalsAgainst,
                GoalsDifference
            FROM {SQLITE_TABLE_HOCKEY_RESULTS}
        """).fetchall()
        conn.close()
        return [
            HockeyTeamResultsDict(
                TeamName=item[0],
                Year=item[1],
                Wins=item[2],
                Losses=item[3],
                OTLosses=item[4],
                WinPct=item[5],
                GoalsFor=item[6],
                GoalsAgainst=item[7],
                GoalsDifference=item[8],
            )
            for item in data
        ]
    
    @ttl_cache(maxsize=1, ttl=5)
    def get_win_pct_data(self) -> List[HockeyTeamResultsDict]:
        # ! TODO !
        # Change this function to return the team with the highest win percentage for each year.
        # If you know SQL, write a query to get this directly from SQLite.
        # If you don't, you can just do it in Python by calling `get_all_data()` above.
        return []
