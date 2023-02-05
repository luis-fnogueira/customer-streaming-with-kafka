# Streaming of customers registering using Kafka
### This project simulates the streamings of users signing up on a website. I use an [open API](https://random-data-api.com/documentation) to request data and send them to a Kafka topic as it were new customers signing up.
### My goal was to create a modular code to manage these situations, following SOLID best practices and a documented code.



# 1. Creating the topic

After building the containers with `docker-compose up -d` it's necessary to open the **broker** bash and create a Kafka topic.

### Opening broker CLI
`docker exec -it broker bash`
### Creating an topic with 10 partitions
`kafka-topics --bootstrap-server localhost:9092 --topic user-tracker --create --partitions 10 --replication-factor 1`             


# 2. Producing data

I decided to separate the "creation" of data to the actual production of data into Kafka. Then I created the `get_data` function to request data from the API and the `send_message` function to actually send this data to a topic.

## 2.1 get_data

    # Manages the connections
    http = urllib3.PoolManager()

    # If the function catches an HTTPError, it will retry 4 times
    @retry(exceptions=HTTPError, tries=4, delay=3, backoff=2)
        def get_data(url: str):

        # Defining URL, if it returns a status different than 200, it'll raise an error
        url = http.request(method="GET", url=r"https://random-data-api.com/api/v2/users")

        if url.status != 200:

            raise HTTPError

        try:

            value = url.data.decode("utf-8")

            return value

        except (json.JSONDecodeError, HTTPError):
            return url.data.decode("utf-8")

## 2.2 send_message

    def send_message(message: str, host: dict, topic: str, partition: int):

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
        p.produce(topic=topic, value=message, callback=receipt, partition=partition)

        # blocking producer until previous messaged have been delivered effectively, to make it synchronous.
        p.flush()

### 2.2.1 Callback function
This callback function write logs and prints them.
    import logging

    # Configurint logs to be appended in a producer.log file
    logging.basicConfig(
        format="%(asctime)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="producer.log",
        filemode="w",
    )

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)


    def receipt(err, msg):

        """
        Define a callback function that takes care of acknowledging new messages or errors.
        When a valid message becomes available, it is decoded to utf-8 and printed
        in the preferred format. The same message is also appended to the logs file.

        Arguments:
            err: any.
                An error, if there is any
            msg: any.
                The message that was sent to the topic
        Returns:
            Nothing, it prints what message was sent and in which topic
        """

        if err is not None:
            print(f"Error: {err}")

        else:
            message = f"Produced message on topic {msg.topic} with value of {msg.value().decode('utf-8')}\n"
            logger.info(message)
            print(message)

## 2.3 Instantiating these functions

After declaring these functions, I used them in the `message_sender.py` file. I request data using `ThreadPoolExecutor` to utilize multithreading in those requests. Data is sent into random partitions using Numpy function `randint`.

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

# 3. Consuming messages

## 3.1 message_consumer
In order to consume these messages I created a function called `message_consumer`. It keeps printing messages on the terminal after running `python3 consumer.py`.

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

## 3.2 message_reader
To effectively read those messages I ran the above function on the `message_reader.py` file. It implements correctly this function.

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

