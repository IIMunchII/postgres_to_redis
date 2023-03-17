from dataclasses import dataclass, field
import json
import enum
import numpy as np


class OperationEnum(enum.Enum):
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


@dataclass
class ReplicationData:
    table: str = field(default_factory=str)
    operation: OperationEnum = field(default_factory=OperationEnum.INSERT)
    fields: dict[dict] = field(default_factory=dict)

    def __post_init__(self):
        if not isinstance(self.operation, OperationEnum):
            try:
                self.operation = OperationEnum(self.operation)
            except ValueError as error:
                raise error

    @property
    def key(self):
        return f"{self.table}:{self.row_id}"

    @property
    def row_id(self):
        try:
            return self.fields["id"]["value"]
        except KeyError:
            raise KeyError(
                "Expected fieldname 'id' in fields data. Make sure data has primary field named 'id'"
            )

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            fieldname: value.get("value") for fieldname, value in self.fields.items()
        }

    def to_redis(self):
        result_dictionary = self.to_dict()
        return arrays_to_bytes(result_dictionary)


def arrays_to_bytes(dictionary: dict):
    for key, value in dictionary.items():
        if isinstance(value, np.ndarray):
            dictionary.update({key: value.astype(np.float32).tobytes()})
        if isinstance(value, list):
            dictionary.update({key: np.array(value).astype(np.float32).tobytes()})
    return dictionary


if __name__ == "__main__":
    replication_data = ReplicationData(
        "article",
        "INSERT",
        {
            "id": {"value": 2, "type": "integer"},
            "vector": {"value": [1, 2, 3, 4], "type": "array"},
            "title": {"value": "Some title", "type": "text"},
        },
    )
    print(replication_data)
    print(replication_data.to_json())
