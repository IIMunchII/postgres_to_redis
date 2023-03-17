import re
import json
from data import ReplicationData
from typing import Protocol


class ReplicationParser(Protocol):
    def parse(self) -> ReplicationData:
        ...


class TestDecodingParser:
    def extract_table_operation_fields(self, message: str):
        pattern = r"table public\.(\w+): (?:)(\w+): (.+)"
        match = re.search(pattern, message)

        if not match:
            return None

        return match.group(1), match.group(2), match.group(3)

    def extract_field_matches(self, fields_str):
        field_pattern = r"(\w+)\[(.+?)\]:(.*?)(?:\s|$)"
        return re.findall(field_pattern, fields_str)

    def parse_field(self, field_type, field_value):
        if field_type == "integer":
            value = int(field_value)
        elif field_type == "character varying":
            value = field_value.strip("'")
        elif field_type == "text":
            value = field_value.strip("'")
        elif field_type == "double precision[]":
            value = json.loads(
                field_value.strip("'").replace("{", "[").replace("}", "]")
            )
        else:
            value = field_value

        return {
            "type": field_type,
            "value": value,
        }

    def parse(self, message: str) -> ReplicationData:
        table_operation_fields = self.extract_table_operation_fields(message)

        if not table_operation_fields:
            return None

        table, operation, fields_str = table_operation_fields
        field_matches = self.extract_field_matches(fields_str)

        fields = {
            field_name: self.parse_field(field_type, field_value)
            for field_name, field_type, field_value in field_matches
        }

        return ReplicationData(
            **{
                "table": table,
                "operation": operation,
                "fields": fields,
            }
        )


if __name__ == "__main__":
    replication_message = """
    table public.article: INSERT: id[integer]:124 vector[double precision[]]:'{-0.44293891736918733,0.46252013300874983,-0.8958587649824163,-0.7730148573287148}' title[character varying]:'Audience among discover imagine great.' body[text]:'Official page series commercial win have seven water. Wait name adult important worry arm well. Actually bag get others rule item.' subtitle[text]:'Movement there cut service network.'
    """
    parser = TestDecodingParser()
    result = parser.parse(replication_message)
    print(result)
