import redis
import numpy as np
from postgres_replicator.search import create_nn_query, search, create_filter_in_string
from postgres_replicator.redis_setup import create_index, get_flat_index_field

if __name__ == "__main__":
    client = redis.Redis()

    search_index = client.ft("article_index")
    vector_field = get_flat_index_field("vector", 10_000)

    try:
        create_index(search_index, vector_field)
    except redis.exceptions.ResponseError as error:
        print(error, "- Skipping creation of index")

    query_vector = np.random.random((1, 500)).astype(np.float32).tobytes()

    query, params = create_nn_query(
        top_k=5,
        vector_field_name="vector",
        query_vector=query_vector,
        return_fields=["id", "title", "subtitle"],
        filter=create_filter_in_string(
            "id", [24713, 28641, 14089, 29115, 25650, 12124, 14959]
        ),
    )

    search_index = client.ft("article_index")
    result = search(
        search_index,
        query,
        params,
    )
    print(result)
