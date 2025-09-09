import os

from elasticsearch import ApiError
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
            return file_path
        except Exception as e:
            self._logger.error(f"Failed to write file: {e}")

    def _transcribe_file(self, file_path):
        try:
            self._logger.info(f"Transcribing file in: {file_path}")
            result, info = self._transcriber.transcribe_audio(file_path)
            result_str = ""
            for segment in result:
                result_str += segment.text
            self._logger.info(
                f"file in {file_path} transcribed successfully! Language detected: {info.language}, probability: {info.language_probability:.2%}")
            return result_str, info
        except Exception as e:
            self._logger.error(f"Failed to transcribe file in {file_path}: {e}")

    def _update_transcription_to_es(self, file_id, transcription, info):
        try:
            document = {
                "transcribed_text": transcription,
                "text_language": info.language,
                "language_probability": info.language_probability
            }
            self._es_client.update_document(file_id, document)
            self._logger.info(f"Updated transcription to Elastic fo file id: {file_id}")
        except ApiError as e:
            self._logger.error(f"Failed to update message {file_id} to Elastic: {e}")
        except Exception as e:
            self._logger.error(f"An unexpected error occurred while processing massage {file_id}: {e}")

    async def get_and_transcribe_data(self):
        """Transcribe the data consumed from Kafka."""
        for msg in self._consumer.get_consumed_messages():
            unique_id = msg.value['unique_id']
            self._logger.info(f"Processing consumed message file {unique_id} for transcription")
            file_data = await self._get_file_from_db(unique_id)
            if file_data is None:
                self._logger.error(f'No data found for file id {unique_id}')
                continue
            file_path = self._write_file_locally(unique_id, file_data)
            transcription, info = self._transcribe_file(file_path)
            self._update_transcription_to_es(unique_id, transcription, info)
