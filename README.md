# How to start.
Please use python3.11

# Install package

```bash
pip install .
```

# Run redis and postgresql
Make sure not to have something allready running on default ports.

```bash
docker compose up -d
```

# Start consumer/subscriber
This command will create a replication slot and start subscribing to database changes.
```bash
python main.py
```

# Insert some data
This will start inserting 50.000 rows of into the database. Vector dimensions will be 500 and float32. The consumer class will do replication to the Redis instance. Redis data is stored as hashed fields using an index with RedisSearch (Example for using RedisJson is not yet done).
```bash
python insert_data.py
```

# Run search example
This will run a search example by randomly generating ids between 1-50.000.
It will first get the vector from one id (similarity article) then generate 250 candidate articles from which similarity to one article is wanted. And then perform the search. The timeit function will give results on search time.
```bash
python search_example.py
```

# Mermaid class diagram
```mermaid
classDiagram
    class LogicalStreamConsumer {
        -parser: ReplicationParser
        -replicator: Replicator
        +__init__(parser: ReplicationParser, replicator: Replicator)
        +__call__(message: ReplicationMessage): void
        +process_message(payload: str): void
    }
    class ReplicationParser {
        +parse(payload: str): ReplicationData
    }
    class Replicator {
        +replicate(replication_data: ReplicationData): None
    }
    class ReplicationMessage {
        -payload: str
        -cursor: Cursor
        -data_start: int
    }
    class Cursor {
        +send_feedback(flush_lsn: int): None
    }
    class ReplicationData {
        -table: str
        -action: str
        -data: Dict[str, Any]
    }
    LogicalStreamConsumer -> ReplicationParser
    LogicalStreamConsumer -> Replicator
    LogicalStreamConsumer --> ReplicationMessage
    ReplicationMessage --> Cursor
    ReplicationParser --> ReplicationData
    Replicator --> ReplicationData
```
