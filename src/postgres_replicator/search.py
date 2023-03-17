import numpy as np
from redis.commands.search.query import Query, Filter
from redis.commands.search import Search


def create_nn_query(
    top_k: int,
    vector_field_name: str,
    query_vector: np.ndarray,
    return_fields: list[str],
    *args,
    **kwargs,
) -> tuple[Query, dict]:
    return_fields.append("score")
    query = (
        create_knn_query(top_k, vector_field_name, *args, **kwargs)
        .sort_by("score")
        .return_fields(*return_fields)
        .dialect(2)
    )
    params_dict = {"vec_param": query_vector}
    return query, params_dict


def create_knn_query(top_k, vector_field_name, filter="*") -> Query:
    return Query(f"{filter}=>[KNN {top_k} @{vector_field_name} $vec_param AS score]")


def create_filter_in_string(fieldname: str, value_list: list[int]) -> Filter:
    return f"@{fieldname}:({__create_pipe_separated_string(value_list)})"


def __create_pipe_separated_string(int_list):
    return "|".join(map(str, int_list))


def search(
    search_index: Search,
    query: Query,
    params_dict,
):
    return search_index.search(
        query,
        query_params=params_dict,
    )
