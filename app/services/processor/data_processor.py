from core import Database
from dal import PodcastsDal
from elasticsearch import ApiError
from kafka.errors import NoBrokersAvailable, KafkaError
from models import Consumer, ElasticSearchClient, Logger, Producer
from pymongo.errors import PyMongoError
from utils.data_hash import DataHash


class DataProcessor:
    """The data processor service class."""

    def __init__(self, kafka_broker, kafka_topic):
        """Constructor."""
        self._consumer = Consumer(kafka_topic, kafka_broker)
        self._producer = Producer(kafka_broker)
        self._es_client = ElasticSearchClient(kafka_topic)
        self._dal = PodcastsDal(Database())
        self._logger = Logger.get_logger()

    def _add_unique_id(self, msg):
        """Adds a hashed unique ID to the message based on its metadata."""
        msg_str = f'{msg["name"] + msg["created_at"] + str(msg["size_in_bytes"]) + msg["file_type"]}'
        msg["unique_id"] = DataHash().hash_file(msg_str)
        return msg

    async def _insert_file_to_db(self, msg):
        """Inserts a file into the database."""
        try:
            await self._dal.insert_document("podcasts", msg)
            self._logger.info(f"Inserted file id {msg["unique_id"]} to MongoDB.")
        except PyMongoError as e:
            self._logger.error(f"Failed to insert message {msg["unique_id"]} to MongoDB: {e}")
        except Exception as e:
            self._logger.error(f"An unexpected error occurred while processing massage {msg["unique_id"]}: {e}")

    def _insert_msg_to_es(self, msg):
        """Inserts a message into the ElasticSearch index."""
        try:
            self._es_client.load_to_es(msg)
            self._logger.info(f"Inserted message id {msg["unique_id"]} to Elastic.")
        except ApiError as e:
            self._logger.error(f"Failed to insert message {msg["unique_id"]} to Elastic: {e}")
        except Exception as e:
            self._logger.error(f"An unexpected error occurred while processing massage {msg["unique_id"]}: {e}")

    def _publish_message_to_transcription(self, msg):
        """Publishes a message to the Kafka broker for transcription."""
        self._producer.publish_massage("transcribe", msg)  # TODO: make the topic without hardcoded values maybe.
        self._logger.info(f"Published message id {msg["unique_id"]} to Kafka for transcription.")

    async def process(self):
        """Processes messages from the consumer."""
        try:
            for msg in self._consumer.get_consumed_messages():
                self._logger.info(f"Processing consumed message file {msg.value['name']} for procession")
                msg_dict = self._add_unique_id(msg.value)
                self._insert_msg_to_es(msg_dict)
                await self._insert_file_to_db(msg_dict)
                self._publish_message_to_transcription({"unique_id": msg_dict["unique_id"]})

        except NoBrokersAvailable as e:
            self._logger.error(f"Kafka connection error: {e}")
        except KafkaError as e:
            self._logger.error(f"Kafka error during consumption: {e}")
        except Exception as e:
            self._logger.error(f"Unexpected error: {e}")
