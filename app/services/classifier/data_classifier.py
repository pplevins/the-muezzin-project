from app.models import Consumer, ElasticSearchClient, Logger
from app.utils import TextClassifier


class DataClassifier:
    def __init__(self, kafka_topic, kafka_url, index_name):
        self._classifier = TextClassifier()
        self._consumer = Consumer(kafka_topic, kafka_url)
        self._es_client = ElasticSearchClient(index_name)
        self._logger = Logger.get_logger()
