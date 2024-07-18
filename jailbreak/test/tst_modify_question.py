import requests, pprint
import json

payload = """
        {
            "id": 203,
            "data":{
                "target": "预期回复3",
                "behavior": "问题简称3"
            }
        }
    """
# payload = json.dumps(payload)

response = requests.post('http://localhost/api/modify-question', data=payload)

pprint.pprint(response.json())