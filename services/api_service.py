import requests

API = "http://localhost:8000"
EDTEndpoint = "/uvsq/edt/{classe}+{start}+{end}"
BULLETINSEndpoint = "/uvsq/bulletin/{id}+{password}"
AUTOCOMPLETEEndpoint = "/uvsq/classe/{query}"

def get_edt_data(classe, start, end):
    response = requests.get(
        API + EDTEndpoint.format(classe=classe, start=start, end=end)
    )
    return response.json()

def login(id, password):
    response = requests.get(API + BULLETINSEndpoint.format(id=id, password=password))
    return response.json()

def autocomplete(query):
    response = requests.get(API + AUTOCOMPLETEEndpoint.format(query=query))
    return response.json()