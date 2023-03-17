import psycopg2
import redis
from psycopg2.extras import RealDictCursor

from postgres_replicator.backfillers import RedisBackfiller


def create_connection():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432",
        cursor_factory=RealDictCursor,
    )


if __name__ == "__main__":
    client = redis.Redis()
    redis_backfiller = RedisBackfiller(
        client=client,
        table="article",
        key_field="id",
    )
    with create_connection() as conn:
        query = "SELECT * FROM article;"
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            redis_backfiller.backfill(result)
