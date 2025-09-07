import asyncio
import os

from app.services.processor.data_processor import DataProcessor


async def main():
    processor = DataProcessor(os.environ['KAFKA_BROKER'], [os.environ['KAFKA_TOPIC']])
    await processor.process()


if __name__ == '__main__':
    asyncio.run(main())
