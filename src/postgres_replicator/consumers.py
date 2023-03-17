from parsers import TestDecodingParser
from psycopg2.extras import ReplicationMessage
from parsers import ReplicationParser
from replicators import Replicator


class LogicalStreamConsumer:
    def __init__(self, parser: ReplicationParser, replicator: Replicator):
        self.parser = parser
        self.replicator = replicator

    def __call__(self, message: ReplicationMessage):
        if message.payload:
            self.process_message(message.payload)
        message.cursor.send_feedback(flush_lsn=message.data_start)

    def process_message(self, payload: str):
        if payload.startswith("BEGIN") or payload.startswith("COMMIT"):
            print(payload)
        else:
            print(payload)
            replication_data = self.parser.parse(payload)
            print(replication_data)
            self.replicator.replicate(replication_data)
