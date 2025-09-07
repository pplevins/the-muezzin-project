import os

from app.models import Consumer


def main():
    consumer = Consumer(os.environ['KAFKA_TOPIC'], os.environ['KAFKA_BROKER'])
    for data in consumer.get_consumed_messages():
        print(data)


if __name__ == '__main__':
    main()
