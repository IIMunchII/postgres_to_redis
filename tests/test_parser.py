from postgres_replicator.parsers import TestDecodingParser
from postgres_replicator.data import ReplicationData

expected_result = ReplicationData(
    table="article",
    operation="INSERT",
    fields={
        "id": {"type": "integer", "value": 124},
        "vector": {
            "type": "double precision[]",
            "value": [
                -0.44293891736918733,
                0.46252013300874983,
                -0.8958587649824163,
                -0.7730148573287148,
            ],
        },
        "title": {
            "type": "character varying",
            "value": "Audience among discover imagine great.",
        },
        "body": {
            "type": "text",
            "value": "Official page series commercial win have seven water. Wait name adult important worry arm well. Actually bag get others rule item.",
        },
        "subtitle": {"type": "text", "value": "Movement there cut service network."},
    },
)


def test_decoding_parser():
    replication_message = """
    table public.article: INSERT: id[integer]:124 vector[double precision[]]:'{-0.44293891736918733,0.46252013300874983,-0.8958587649824163,-0.7730148573287148}' title[character varying]:'Audience among discover imagine great.' body[text]:'Official page series commercial win have seven water. Wait name adult important worry arm well. Actually bag get others rule item.' subtitle[text]:'Movement there cut service network.'
    """
    parser = TestDecodingParser()
    result = parser.parse(replication_message)

    assert result.fields == expected_result.fields
    assert result.operation == expected_result.operation
    assert result.table == expected_result.table
