import os

from pymongo.errors import PyMongoError

from app.core import Database
from app.dal import PodcastsDal
from app.models import Consumer, ElasticSearchClient, Logger
from app.utils import AudioTranscriber


class DataTranscriber:
    def __init__(self, kafka_url, kafka_topic, index_name):
        """Constructor."""
        self._consumer = Consumer(kafka_topic, kafka_url)
        self._dir_path = '/tmp/muezzin-data'  # TODO: Remember to delete afterwards
        os.makedirs(self._dir_path, exist_ok=True)
        self._es_client = ElasticSearchClient(index_name)
        self._dal = PodcastsDal(Database())
        self._logger = Logger.get_logger()
        self._transcriber = AudioTranscriber()

    async def _get_file_from_db(self, file_id):
        try:
            file_data = await self._dal.find_document(file_id)
            return file_data
        except PyMongoError as e:
            self._logger.error(f"Failed to find document {file_id} from MongoDB: {e}")
        except Exception as e:
            self._logger.error(f"An unexpected error occurred while processing document {file_id}: {e}")

    def _write_file_locally(self, file_id, data):
        try:
            file_path = os.path.join(self._dir_path + '/' + file_id + '.wav')
            self._logger.info(f"Writing file to disk in: {file_path}")
            with open(file_path, 'w+b') as file:
                file.write(data)
        except Exception as e:
            self._logger.error(f"Failed to write file: {e}")

    async def get_and_transcribe_data(self):
        """Transcribe the data consumed from Kafka."""
        for msg in self._consumer.get_consumed_messages():
            unique_id = msg.value['unique_id']
            self._logger.info(f"Processing consumed message file {unique_id} for transcription")
            file_data = await self._get_file_from_db(unique_id)
            if file_data is None:
                self._logger.error(f'No data found for file id {unique_id}')
                continue
            self._write_file_locally(unique_id, file_data)
