from flask import Flask, request
from concurrent.futures import ProcessPoolExecutor
import requests
import logging


app = Flask(__name__)

MAX_THREADS = 100


# Function to send request
def fetch_url_data(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    else:
        logging.warning(f"There was an error with status code: {r.status_code} while trying to get data from: {url}")
        return {}


@app.route("/", methods=['GET'])
def social_network_activity():
    if request.method == 'GET':
        # Urls to query
        urls = ["https://takehome.io/instagram", "https://takehome.io/facebook", "https://takehome.io/twitter"]

        # Create thread executor with number of threads
        executor = ProcessPoolExecutor(MAX_THREADS)

        # Iterate over the urls and append each to thread of the future dict
        futures = []
        for url in urls:
            future = executor.submit(fetch_url_data, url)
            futures.append(future)

        # Iterate over threads results and append to single response
        all_response = []
        for future in futures:
            all_response.append(future.result())

        # Format the response
        json_response = {
            'instagram': len(all_response[0]),
            'facebook': len(all_response[1]),
            'twitter': len(all_response[2])
        }

        return json_response
