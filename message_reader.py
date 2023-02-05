from consumer import message_consumer


consumer = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "python-consumer",
    "auto.offset.reset": "earliest",
}

print("Kafka Consumer has been initiated...")
