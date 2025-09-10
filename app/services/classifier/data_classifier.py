from elasticsearch import ApiError
from kafka.errors import NoBrokersAvailable, KafkaError

from app.models import Consumer, ElasticSearchClient, Logger
from app.utils import TextClassifier


class DataClassifier:
    def __init__(self, kafka_topic, kafka_url, index_name):
        self._classifier = TextClassifier()
        self._consumer = Consumer(kafka_topic, kafka_url)
        self._es_client = ElasticSearchClient(index_name)
        self._logger = Logger.get_logger()

    def _update_transcription_to_es(self, file_id, document):
        """Updates the classification to ElasticSearch."""
        try:
            self._es_client.update_document(file_id, document)
            self._logger.info(f"Updated classification to Elastic fo file id: {file_id}")
        except ApiError as e:
            self._logger.error(f"Failed to update message {file_id} to Elastic: {e}")
        except Exception as e:
            self._logger.error(f"An unexpected error occurred while processing massage {file_id}: {e}")

    def get_and_classify_data(self):
        """Classify data from Kafka."""
        try:
            for msg in self._consumer.get_consumed_messages():
                unique_id = msg.value['unique_id']
                self._logger.info(f"Processing consumed message file {unique_id} for classification")
                text = msg.value['transcription']
                print(text)
                classification_result = self._classifier.classify_text(text)
                self._logger.info(
                    f"Classification result for file id {unique_id}: bds_precent: {classification_result['bds_precent']:.2%}, is_bds: {classification_result['is_bds']}, bds_threat_level: {classification_result['bds_threat_level']}")
                self._update_transcription_to_es(unique_id, classification_result)

        except NoBrokersAvailable as e:
            self._logger.error(f"Kafka connection error: {e}")
        except KafkaError as e:
            self._logger.error(f"Kafka error during consumption: {e}")
        except Exception as e:
            self._logger.error(f"Unexpected error: {e}")
