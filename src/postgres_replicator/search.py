import numpy as np
import redis
from redis.commands.search.query import Query
from redis.commands.search import Search


def create_nn_query(
    top_k: int,
    vector_field_name: str,
    query_vector: np.ndarray,
    return_fields: list[str],
):
    return_fields.append("score")
    query = (
        Query(f"*=>[KNN {top_k} @{vector_field_name} $vec_param AS score]")
        .sort_by("score")
        .return_fields(*return_fields)
        .dialect(2)
    )
    params_dict = {"vec_param": query_vector}
    return query, params_dict


def search(
    search_index: Search,
    query: Query,
    params_dict,
):
    return search_index.search(
        query,
        query_params=params_dict,
    )


if __name__ == "__main__":
    client = redis.Redis()
    query_vector = np.random.random((1, 500)).astype(np.float32).tobytes()
    query, params = create_nn_query(
        top_k=5,
        vector_field_name="vector",
        query_vector=query_vector,
        return_fields=["id", "title", "subtitle"],
    )
    # query = Query("*=>[KNN 2 @vector $vec]").return_field("__v_score").dialect(2)
    # params = {"vec": query_vector}
    search_index = client.ft("article_index")
    result = search(
        search_index,
        query,
        params,
    )
    print(result)

# q = (
#     Query(f"*=>[KNN {topK} @{ITEM_KEYWORD_EMBEDDING_FIELD} $vec_param AS vector_score]")
#     .sort_by("vector_score")
#     .paging(0, topK)
#     .return_fields("vector_score", "item_name", "item_id", "item_keywords", "country")
#     .dialect(2)
# )
# params_dict = {"vec_param": query_vector}
