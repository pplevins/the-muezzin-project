from elasticsearch import ApiError
from kafka.errors import NoBrokersAvailable, KafkaError
from pymongo.errors import PyMongoError

from app.core import Database
from app.dal import PodcastsDal
from app.models import Consumer, ElasticSearchClient, Logger
from app.utils import DataHash


class DataProcessor:
    def __init__(self, kafka_broker, kafka_topic):
        self._consumer = Consumer(kafka_topic, kafka_broker)
        self._es_client = ElasticSearchClient(kafka_topic)
        self._dal = PodcastsDal(Database())
        self._logger = Logger.get_logger()

    def _add_unique_id(self, msg):
        msg_str = f'{msg["name"] + msg["created_at"] + str(msg["size_in_bytes"]) + msg["file_type"]}'
        msg["unique_id"] = DataHash().hash_file(msg_str)
        return msg

    async def _insert_file_to_db(self, msg):
        await self._dal.insert_document("podcasts", msg)

    async def process(self):
        try:
            for msg in self._consumer.get_consumed_messages():
                try:
                    msg_dict = self._add_unique_id(msg.value)
                    self._es_client.load_to_es(msg_dict)
                    self._logger.info(f"Inserted message id {msg_dict["unique_id"]} to Elastic.")
                    await self._insert_file_to_db(msg_dict)
                    self._logger.info(f"Inserted file id {msg_dict["unique_id"]} to MongoDB.")

                except ApiError as e:
                    self._logger.error(f"Failed to insert message {msg.value} to Elastic: {e}")
                except PyMongoError as e:
                    self._logger.error(f"Failed to insert message {msg.value} to MongoDB: {e}")
                except Exception as e:
                    self._logger.error(f"An unexpected error occurred while processing massage {msg.value}: {e}")

        except NoBrokersAvailable as e:
            self._logger.error(f"Kafka connection error: {e}")
        except KafkaError as e:
            self._logger.error(f"Kafka error during consumption: {e}")
        except Exception as e:
            self._logger.error(f"Unexpected error: {e}")
