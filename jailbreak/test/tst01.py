import requests, pprint
import json

payload = {"data": [{"dataset": "datasetname1", "model": "gpt-3.5-turbo", "evaluate_model": "gpt-3.5-turbo"},
              {"dataset": "datasetname2", "model": "gpt-3.5-turbo", "evaluate_model": "gpt-3.5-turbo"}]}
payload = json.dumps(payload)

response = requests.post('http://localhost/api/run',
              data=payload)

pprint.pprint(response.json())