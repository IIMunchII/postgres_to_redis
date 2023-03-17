from redis.commands.search.field import VectorField
from redis.commands.search.field import TextField
from redis.commands.search import Search


def get_flat_index_field(
    vector_field_name,
    number_of_vectors,
    vector_dimensions=500,
    distance_metric="L2",
) -> VectorField:
    return VectorField(
        vector_field_name,
        "FLAT",
        {
            "TYPE": "FLOAT32",
            "DIM": vector_dimensions,
            "DISTANCE_METRIC": distance_metric,
            "INITIAL_CAP": number_of_vectors,
            "BLOCK_SIZE": number_of_vectors,
        },
    )


def get_hsnw_index_field(
    vector_field_name,
    number_of_vectors,
    vector_dimensions=500,
    distance_metric="L2",
    M=40,
    EF=200,
) -> VectorField:
    return VectorField(
        vector_field_name,
        "HNSW",
        {
            "TYPE": "FLOAT32",
            "DIM": vector_dimensions,
            "DISTANCE_METRIC": distance_metric,
            "INITIAL_CAP": number_of_vectors,
            "M": M,
            "EF_CONSTRUCTION": EF,
        },
    )


def create_index(
    search_index: Search,
    vector_field: VectorField,
):
    search_index.create_index(
        [
            vector_field,
            TextField("title"),
            TextField("subtitle"),
            TextField("body"),
        ]
    )
