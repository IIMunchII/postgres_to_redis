import redis
from more_itertools import chunked
from typing import Protocol
from postgres_replicator.data import arrays_to_bytes


class Backfiller(Protocol):
    def backfill(self, data: list[dict]) -> None:
        ...


class RedisBackfiller:
    def __init__(
        self,
        table: str,
        key_field: str,
        client: redis.Redis,
    ):
        self.table = table
        self.key_field = key_field
        self.client = client

    def backfill(self, data: list[dict]):
        self.__load_data_in_chunks(data)

    def __load_data_in_chunks(
        self,
        data: list[dict],
        chunk_size: int = 10000,
    ):
        for batch in chunked(data, chunk_size):
            pipeline = self.client.pipeline(transaction=False)
            for row in batch:
                pipeline.hset(self.__get_key(row), mapping=arrays_to_bytes(row))
            pipeline.execute()

    def __get_key(self, row: dict):
        return f"{self.table}:{row.get(self.key_field)}"
