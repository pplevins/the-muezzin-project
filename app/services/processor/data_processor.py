from app.core import Database
from app.dal import PodcastsDal
from app.models import Consumer, ElasticSearchClient
from app.utils import DataHash


class DataProcessor:
    def __init__(self, kafka_broker, kafka_topic):
        self._consumer = Consumer(kafka_topic, kafka_broker)
        self._es_client = ElasticSearchClient(kafka_topic)
        self._dal = PodcastsDal(Database())

    def _add_unique_id(self, msg):
        msg_str = f'{msg["name"] + msg["created_at"] + str(msg["size_in_bytes"]) + msg["file_type"]}'
        msg["unique_id"] = DataHash().hash_file(msg_str)
        return msg

    async def _insert_file_to_db(self, msg):
        await self._dal.insert_document("podcasts", msg)

    async def process(self):
        for msg in self._consumer.get_consumed_messages():
            msg_dict = self._add_unique_id(msg.value)
            print(msg_dict)
            self._es_client.load_to_es(msg_dict)
            await self._insert_file_to_db(msg_dict)
