import psycopg
from faker import Faker
import random


def generate_dummy_data(faker):
    vector = [random.uniform(-1, 1) for _ in range(500)]
    title = faker.sentence()
    body = faker.text()
    subtitle = faker.sentence()

    return vector, title, body, subtitle


def insert_article(connection, vector, title, body, subtitle):
    query = """
        INSERT INTO article (vector, title, body, subtitle)
        VALUES (%s, %s, %s, %s)
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (vector, title, body, subtitle))
        connection.commit()


def create_table(conn):
    with conn.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS article (
        id SERIAL PRIMARY KEY,
        vector double precision[500],
        title VARCHAR(200),
        body TEXT,
        subtitle TEXT
        );
        """
        )
        conn.commit()


if __name__ == "__main__":
    faker = Faker()

    with psycopg.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432",
    ) as conn:
        create_table(conn)
        vector, title, body, subtitle = generate_dummy_data(faker)

        insert_article(conn, vector, title, body, subtitle)
