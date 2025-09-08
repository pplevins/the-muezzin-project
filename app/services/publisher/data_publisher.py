from app.models import Producer
from app.utils import MetadataExtractor


class DataPublisher:
    """The Data Publisher service class."""

    def __init__(self, kafka_url, files_dir):
        """Constructor."""
        self._producer = Producer(kafka_url)
        self._extractor = MetadataExtractor(files_dir)

    def extract_and_publish(self, topic):
        """Extract the metadata from all the files, and publish it to a given topic in Kafka."""
        for file in self._extractor.get_all_in_dir():
            metadata = self._extractor.extract_metadata(file)
            self._producer.publish_massage(topic, metadata)
