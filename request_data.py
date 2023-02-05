import json
import urllib3
from retry import retry
from urllib.error import HTTPError
from concurrent.futures import ThreadPoolExecutor


http = urllib3.PoolManager()

# If the function catches an HTTPError, it will retry 4 times
@retry(exception=HTTPError, tries=4, delay=3, backoff=2)
def get_data(url: str):

    # Defining URL, if it returns a status different than 200, it'll raise an error
    url = http.request(method='GET', url=r'https://random-data-api.com/api/v2/users')

    if url.status != 200:
        
        raise HTTPError

    try:

        value = json.loads(url.data.decode('utf-8'))
        
        return value

    except (json.JSONDecodeError, HTTPError):
        return url.data.decode('utf-8')



all_results = []
with ThreadPoolExecutor(max_workers=80) as executor:
        all_numbers = []
        for i in range(0, 50):
            all_numbers.append(i)

        
        for i in executor.map(get_data, all_numbers):
            print(i)

