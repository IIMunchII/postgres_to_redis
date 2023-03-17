import redis
import numpy as np
from postgres_replicator.search import create_nn_query, search, create_filter_in_string
from postgres_replicator.redis_setup import create_index, get_flat_index_field
import random

if __name__ == "__main__":
    client = redis.Redis()

    search_index = client.ft("article_index")
    vector_field = get_flat_index_field("vector", 10_000)

    try:
        create_index(search_index, vector_field)
    except redis.exceptions.ResponseError as error:
        print(error, "- Skipping creation of index")

    candidate_list = [random.randint(1, 50_000) for _ in range(250)]
    article_id = random.randint(1, 50_000)
    query_vector = client.hget(f"article:{article_id}", "vector")

    query, params = create_nn_query(
        top_k=5,
        vector_field_name="vector",
        query_vector=query_vector,
        return_fields=["title", "subtitle", "id"],
        filter=create_filter_in_string("id", candidate_list),
    )

    search_index = client.ft("article_index")
    result = search(
        search_index,
        query,
        params,
    )
    print(result)


import timeit


def test_search():
    return search(search_index, query, params)


average_query_time = timeit.timeit(test_search, number=1000) / 1000

print(f"Query: {query.query_string()}: Average querytime: {average_query_time}")
