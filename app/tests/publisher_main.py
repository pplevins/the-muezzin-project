import os

from app.services import DataPublisher


def main():
    """The publisher service main function"""
    publisher = DataPublisher(
        kafka_url=os.environ['KAFKA_BROKER'],
        files_dir=os.environ['FILES_DIR'])
    publisher.extract_and_publish(os.environ['KAFKA_TOPIC'])


if __name__ == '__main__':
    # The local running point for the publisher service.

    # NOTE: Make sure to configure all the necessary environment variables,
    # and run all the containers (Kafka etc.) before running.
    main()
