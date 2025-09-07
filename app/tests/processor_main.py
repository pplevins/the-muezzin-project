import os

from app.services.processor.data_processor import DataProcessor


def main():
    processor = DataProcessor(os.environ['KAFKA_BROKER'], [os.environ['KAFKA_TOPIC']])
    processor.process()


if __name__ == '__main__':
    main()
