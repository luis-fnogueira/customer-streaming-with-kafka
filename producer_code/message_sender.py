import numpy as np
from producer import send_message
from request_data import get_data
from concurrent.futures import ThreadPoolExecutor


# Initiating the producer with the Kafka cluster
kafka_port = {"bootstrap.servers": "localhost:9092"}

# Defining which topic will receive the message
topic = "user-tracker"

# Requests where requests will be made
url = "https://random-data-api.com/api/v2/users"

while True:

    with ThreadPoolExecutor(max_workers=80) as executor:

        # Defining URL, if it returns a status different than 200, it'll raise an error
        data = executor.submit(get_data, url)

        # Sending message to the topic in a random partition
        send_message(
            message=data.result(),
            host=kafka_port,
            topic=topic,
            partition=np.random.randint(0, 10),
        )
