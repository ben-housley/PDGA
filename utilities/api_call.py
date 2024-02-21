import requests
import json


def make_api_call_get(api_url):
    return requests.get(api_url)