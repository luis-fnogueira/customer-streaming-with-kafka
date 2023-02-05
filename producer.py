from receipt import receipt
from confluent_kafka import Producer


def send_message(message: str, host: dict):

    """
    This function sends message to topic on Kafka.

    Arguments:
        message: str.
            The message that will be sent to the topic.
        producer: dict
            The port of Kafka cluster, like: {'bootstrap.servers':'localhost:9092'}
    Returns:
        It dumps a message into a topic
    """

    p = Producer(host)

    # Request any previous events to the producer. If found, events are sent to the callback function
    p.poll(1)

    # Effectively sends message
    p.produce(topic="user-tracker", value=message, callback=receipt)

    # blocking producer until previous messaged have been delivered effectively, to make it synchronous.
    p.flush()
