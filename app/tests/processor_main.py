import asyncio
import os

from processor import DataProcessor


async def main():
    """The processor service main function"""
    processor = DataProcessor(os.environ['KAFKA_BROKER'], [os.environ['KAFKA_TOPIC']])
    await processor.process()


if __name__ == '__main__':
    # The local running point for the processor service.

    # NOTE: Make sure to configure all the necessary environment variables,
    # and run all the containers (Kafka, MongoDB, ElasticSearch etc.) before running.
    asyncio.run(main())
