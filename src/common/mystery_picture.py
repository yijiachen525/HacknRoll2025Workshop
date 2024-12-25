import sqlite3
from typing import TypedDict, List

from cachetools.func import ttl_cache

from settings import SQLITE_DATABASE, DB_PATH, SQLITE_TABLE_MYSTERY_PICTURE

SQLITE_MAX_ARGS = 100


class MysteryPictureDict(TypedDict):
    X: int
    Y: int
    Value: int


class MysteryPicture:
    def create_table(self):
        conn = sqlite3.connect(f"{DB_PATH}/{SQLITE_DATABASE}.db")
        conn.execute(f"""
            DROP TABLE IF EXISTS {SQLITE_TABLE_MYSTERY_PICTURE}
        """)
        conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {SQLITE_TABLE_MYSTERY_PICTURE} (
                X INT NOT NULL,
                Y INT NOT NULL,
                Value INT NOT NULL,
                LastUpdateDateUtc DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

                PRIMARY KEY(X, Y)
            )
        """)
        conn.close()

    def insert_data(self, data: List[MysteryPictureDict]) -> None:
        if len(data) > 0:
            args_per_item = len(data[0])
            batch_size = SQLITE_MAX_ARGS // args_per_item
            print("into db")

            conn = sqlite3.connect(f"{DB_PATH}/{SQLITE_DATABASE}.db")
            conn.execute("BEGIN TRANSACTION")
            for i in range(0, len(data), batch_size):
                data_to_insert = data[i:i + batch_size]
                params = [
                    (
                        item["X"],
                        item["Y"],
                        item["Value"],
                    )
                    for item in data_to_insert
                ]
                print(params)

                conn.executemany(f"""
                    INSERT OR REPLACE INTO {SQLITE_TABLE_MYSTERY_PICTURE} (
                        X,
                        Y,
                        Value
                    ) VALUES (?, ?, ?)
                """, params)
            conn.commit()
            conn.close()

    @ttl_cache(maxsize=1, ttl=5)
    def get_all_data(self) -> List[MysteryPictureDict]:
        conn = sqlite3.connect(f"{DB_PATH}/{SQLITE_DATABASE}.db")
        data = conn.execute(f"""
            SELECT
                X,
                Y,
                Value
            FROM {SQLITE_TABLE_MYSTERY_PICTURE}
        """).fetchall()
        conn.close()
        return [
            MysteryPictureDict(
                X=item[0],
                Y=item[1],
                Value=item[2],
            )
            for item in data
        ]
