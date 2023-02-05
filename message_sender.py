import numpy as np
from producer import send_message
from request_data import get_data
from concurrent.futures import ThreadPoolExecutor


# Initiating the producer with the Kafka cluster
kafka_port = {"bootstrap.servers": "localhost:9092"}

# Defining which topic will receive the message
topic = "user-tracker"

all_results = []
# Requesting data with 200 threads
with ThreadPoolExecutor(max_workers=200) as executor:

    # Creating an array to iterate
    all_numbers = []
    for i in range(0, 200):
        all_numbers.append(i)

    # Effectively sending message to the topic
    for i in executor.map(get_data, all_numbers):

        send_message(
            message=i, host=kafka_port, topic=topic, partition=np.random.randint(0, 10)
        )
