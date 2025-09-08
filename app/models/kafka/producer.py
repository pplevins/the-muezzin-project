import json

from kafka import KafkaProducer


class Producer:
    """A Kafka producer client model class."""

    def __init__(self, bootstrap_servers=None):
        """Constructor."""
        self.bootstrap_servers = bootstrap_servers
        if bootstrap_servers is None:
            self.bootstrap_servers = ['localhost:9092']
        self._client = KafkaProducer(bootstrap_servers=self.bootstrap_servers,
                                     value_serializer=lambda msg:
                                     json.dumps(msg, default=str).encode('utf-8'))

    def publish_massage(self, topic, msg):
        """Publish message to topic."""
        self._client.send(topic, msg)
        self._client.flush()
