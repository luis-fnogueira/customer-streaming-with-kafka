from consumer import message_consumer

# Defining consumer settings
consumer = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "python-consumer",
    "auto.offset.reset": "earliest",
}

# Defining which topics to consume
topic: list = ['user-tracker']


# Requesting messages
message_consumer(topics=topic, consumer=consumer)
