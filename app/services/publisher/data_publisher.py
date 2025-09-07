from app.models import Producer
from app.utils import MetadataExtractor


class DataPublisher:
    def __init__(self, kafka_url, files_dir):
        self._producer = Producer(kafka_url)
        self._extractor = MetadataExtractor(files_dir)

    def extract_and_publish(self, topic):
        for file in self._extractor.get_all_in_dir():
            metadata = self._extractor.extract_metadata(file)
            self._producer.publish_massage(topic, metadata)
