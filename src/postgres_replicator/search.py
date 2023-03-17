import numpy as np
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
