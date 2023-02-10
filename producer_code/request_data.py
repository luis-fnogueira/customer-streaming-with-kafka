import json
import urllib3
from retry import retry
from urllib.error import HTTPError

# Manages the connections
http = urllib3.PoolManager()

# If the function catches an HTTPError, it will retry 4 times
@retry(exceptions=HTTPError, tries=4, delay=3, backoff=2)
def get_data(url: str):

    """
    This function makes a GET request to the url passed in the arguments.

    Arguments:
        url: str.
        The url where the request will be made.

    Returns:

        The data decoded in utf-8.
    """

    # Defining URL, if it returns a status different than 200, it'll raise an error
    url = http.request(method="GET", url=f"{url}")

    if url.status != 200:

        raise HTTPError

    try:

        value = url.data.decode("utf-8")

        return value

    except (json.JSONDecodeError, HTTPError):
        return url.data.decode("utf-8")
