from confluent_kafka import Consumer


def message_consumer(topics: list, consumer: dict):

    """
    This function acts as a consumer of a Kafka topic. If there are no messages
    it just keeps waiting. In case of error, it will display it. 

    Arguments:
        Topics: list.
            The topics that will be read.
        Consumer: dict.
            The cluster configurations
    """

    c = Consumer(consumer)

    c.subscribe(topics)

    while True:

        msg = c.poll(1.0)  # timeout
        if msg is None:
            continue
        if msg.error():
            print("Error: {}".format(msg.error()))
            continue
        data = msg.value()
        print(data)
