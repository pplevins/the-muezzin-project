import os

from classifier import DataClassifier


def main():
    """The classifier service main function"""
    classifier = DataClassifier(
        kafka_url=os.environ['KAFKA_BROKER'], kafka_topic=['classification'], index_name='podcasts')
    classifier.get_and_classify_data()


if __name__ == '__main__':
    # The local running point for the classifier service.

    # NOTE: Make sure to configure all the necessary environment variables,
    # and run all the containers (Kafka etc.) before running.
    main()
