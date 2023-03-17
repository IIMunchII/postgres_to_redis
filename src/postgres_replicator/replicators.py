import redis
from postgres_replicator.data import ReplicationData, OperationEnum
from typing import Protocol


class Replicator(Protocol):
    def replicate(self, data: ReplicationData) -> None:
        ...


class RedisReplicator:
    def __init__(self, client: redis.Redis):
        self.client = client

    def replicate(self, data: ReplicationData) -> None:
        if data.operation in (OperationEnum.INSERT, OperationEnum.UPDATE):
            self.__insert_or_update(data)
        if data.operation == OperationEnum.DELETE:
            self.__delete(data)

    def __insert_or_update(
        self,
        data: ReplicationData,
    ):
        self.client.hset(data.key, mapping=data.to_redis())

    def __delete(
        self,
        data: ReplicationData,
    ):
        self.client.hdel(data.key, data.fields.keys())
