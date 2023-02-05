import time
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

        p.poll(1)
        p.produce('user-tracker', message, callback=receipt)
        p.flush()
        time.sleep(3)
