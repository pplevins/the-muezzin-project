from kafka.errors import NoBrokersAvailable, KafkaError

from app.models import Producer, Logger
from app.utils import MetadataExtractor


class DataPublisher:
    """The Data Publisher service class."""

    def __init__(self, kafka_url, files_dir):
        """Constructor."""
        self._producer = Producer(kafka_url)
        self._extractor = MetadataExtractor(files_dir)
        self._logger = Logger.get_logger()

    def extract_and_publish(self, topic):
        """Extract the metadata from all the files, and publish it to a given topic in Kafka."""
        for file in self._extractor.get_all_in_dir():
            try:
                metadata = self._extractor.extract_metadata(file)
                self._producer.publish_massage(topic, metadata)
                self._logger.info(f"Published file {metadata["name"]} to Kafka.")

            except NoBrokersAvailable as e:
                self._logger.error(f"Kafka connection error: {e}")
            except KafkaError as e:
                self._logger.error(f"Kafka error during consumption: {e}")
            except Exception as e:
                self._logger.error(f"Unexpected error: {e}")
