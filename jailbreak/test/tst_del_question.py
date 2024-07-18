import requests, pprint
import json

payload = """
        {
            "id": 203
        }
    """

# payload = json.dumps(payload)

response = requests.post('http://localhost/api/del-question', data=payload)

pprint.pprint(response.json())