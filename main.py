import psycopg2
from psycopg2.extras import LogicalReplicationConnection, REPLICATION_LOGICAL
from postgres_replicator.parsers import TestDecodingParser
from postgres_replicator.consumers import LogicalStreamConsumer
from postgres_replicator.replicators import RedisReplicator
import redis


def create_connection() -> LogicalReplicationConnection:
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432",
        connection_factory=LogicalReplicationConnection,
    )


if __name__ == "__main__":
    redis_client = redis.Redis()
    parser = TestDecodingParser()
    redis_replicator = RedisReplicator(redis_client)
    consumer = LogicalStreamConsumer(parser, redis_replicator)

    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.create_replication_slot("slot1", REPLICATION_LOGICAL, "test_decoding")
    except psycopg2.errors.DuplicateObject as error:
        print(error, "Skipping creation")

    cursor.start_replication("slot1", decode=True, start_lsn="0/0")

    cursor.consume_stream(consumer)
