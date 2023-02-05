import logging

# Configurint logs to be appended in a producer.log file
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='producer.log',
                    filemode='w')

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
        print(f'Error: {err}')

    else:
        message = f"Produced message on topic {msg.topic} with value of {msg.value().decode('utf-8')}\n"
        logger.info(message)
        print(message)