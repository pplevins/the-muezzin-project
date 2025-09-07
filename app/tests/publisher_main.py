import os

from app.services import DataPublisher


def main():
    publisher = DataPublisher(
        kafka_url=os.environ['KAFKA_BROKER'],
        files_dir=os.environ['FILES_DIR'])
    publisher.extract_and_publish(os.environ['KAFKA_TOPIC'])


if __name__ == '__main__':
    main()
