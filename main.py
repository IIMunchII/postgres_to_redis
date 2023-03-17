import psycopg2
from psycopg2.extras import LogicalReplicationConnection, REPLICATION_LOGICAL
from parsers import TestDecodingParser
from consumers import LogicalStreamConsumer
from replicators import RedisReplicator
import redis

if __name__ == "__main__":
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432",
        connection_factory=LogicalReplicationConnection,
    )
    redis_client = redis.Redis()
    parser = TestDecodingParser()
    redis_replicator = RedisReplicator(redis_client)
    consumer = LogicalStreamConsumer(parser, redis_replicator)

    cur = conn.cursor()
    try:
        cur.create_replication_slot("slot1", REPLICATION_LOGICAL, "test_decoding")
    except psycopg2.errors.DuplicateObject as error:
        print(error, "Skipping creation")

    cur.start_replication("slot1", decode=True)

    cur.consume_stream(consumer)
