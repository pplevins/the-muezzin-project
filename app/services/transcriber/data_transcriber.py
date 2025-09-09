import os

from app.core import Database
from app.dal import PodcastsDal
from app.models import Consumer, ElasticSearchClient, Logger


class DataTranscriber:
    def __init__(self, kafka_url, kafka_topic, index_name):
        """Constructor."""
        self._consumer = Consumer(kafka_topic, kafka_url)
        self._file_path = '/tmp/muezzin-data'  # TODO: Remember to delete afterwards
        os.makedirs(self._file_path, exist_ok=True)
        self._es_client = ElasticSearchClient(index_name)
        self._dal = PodcastsDal(Database())
        self._logger = Logger.get_logger()

    async def get_and_transcribe_data(self):
        """Transcribe the data consumed from Kafka."""
        for msg in self._consumer.get_consumed_messages():
            unique_id = msg.value['unique_id']
            file_data = await self._dal.find_document(unique_id)
            if file_data is None:
                self._logger.error(f'No data found for file id {unique_id}')
                continue
            self._logger.info(f'Processing file id {unique_id}')
            with open(self._file_path + '/' + unique_id + '.wav', 'w+b') as file:
                file.write(file_data)
