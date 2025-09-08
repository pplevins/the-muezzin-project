import json

from kafka import KafkaConsumer


class Consumer:
    """A Kafka consumer model class."""

    def __init__(self, topics: list[str], bootstrap_servers=None):
        """Constructor."""
        if bootstrap_servers is None:
            bootstrap_servers = ['localhost:9092']
        self.topics = topics
        self.bootstrap_servers = bootstrap_servers

    def get_consumed_messages(self):
        """Get consumed messages from the subscribed topics."""
        return KafkaConsumer(*self.topics,
                             value_deserializer=lambda msg: json.loads(msg.decode('ascii')),
                             bootstrap_servers=self.bootstrap_servers
                             )
