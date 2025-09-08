import os

from app.core import Database
from app.dal import PodcastsDal
from app.models import Consumer, ElasticSearchClient, Logger


class DataTranscriber:
    def __init__(self, kafka_url, kafka_topic, index_name):
        """Constructor."""
        self._consumer = Consumer(kafka_url, kafka_topic)
        self._file_path = '/tmp/muezzin-data'
        os.makedirs(self._file_path, exist_ok=True)
        self._es_client = ElasticSearchClient(index_name)
        self._dal = PodcastsDal(Database())
        self._logger = Logger.get_logger()
