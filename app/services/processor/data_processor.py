from app.models import Consumer, ElasticSearchClient
from app.utils import DataHash


class DataProcessor:
    def __init__(self, kafka_broker, kafka_topic):
        self._consumer = Consumer(kafka_topic, kafka_broker)
        self._es_client = ElasticSearchClient(kafka_topic)

    def add_unique_id(self, msg):
        msg_str = f'{msg["name"] + msg["created_at"] + str(msg["size_in_bytes"]) + msg["file_type"]}'
        msg["unique_id"] = DataHash().hash_file(msg_str)
        return msg

    def process(self):
        for msg in self._consumer.get_consumed_messages():
            msg_dict = self.add_unique_id(msg.value)
            print(msg_dict)
            self._es_client.load_to_es(msg_dict)
