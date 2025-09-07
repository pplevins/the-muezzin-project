import json

from kafka import KafkaConsumer


class Consumer:
    def __init__(self, topic, bootstrap_servers=None):
        if bootstrap_servers is None:
            bootstrap_servers = ['localhost:9092']
        self.topic = topic
        self.bootstrap_servers = bootstrap_servers

    def get_consumed_messages(self):
        return KafkaConsumer(*self.topic,
                             value_deserializer=lambda msg: json.loads(msg.decode('ascii')),
                             bootstrap_servers=self.bootstrap_servers
                             )
