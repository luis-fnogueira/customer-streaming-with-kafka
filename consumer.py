from confluent_kafka import Consumer


def message_consumer(topics: list, consumer: dict):

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
    c.close()
