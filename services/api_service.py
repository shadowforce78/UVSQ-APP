import requests
from ..constants import API, EDTEndpoint, BULLETINSEndpoint

def get_schedule(classe, start, end):
    response = requests.get(
        API + EDTEndpoint.format(classe=classe, start=start, end=end)
    )
    return response.json()

def login(id, password):
    response = requests.get(
        API + BULLETINSEndpoint.format(id=id, password=password)
    )
    return response.json()