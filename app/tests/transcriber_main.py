import asyncio
import os

from app.services.transcriber.data_transcriber import DataTranscriber


async def main():
    """The transcriber service main function"""
    transcriber = DataTranscriber(os.environ['KAFKA_BROKER'], ["transcribe"], "podcasts")
    await transcriber.get_and_transcribe_data()


if __name__ == '__main__':
    # The local running point for the processor service.

    # NOTE: Make sure to configure all the necessary environment variables,
    # and run all the containers (Kafka, MongoDB, ElasticSearch etc.) before running.
    asyncio.run(main())
