import requests, pprint
import json

payload = """{"data":{"goal": "问题",
        "target": "预期回复",
        "behavior": "问题简称",
        "category": "类别描述"
        }
    }
    """
# payload = json.dumps(payload)

response = requests.post('http://localhost/api/add-question', data=payload)

pprint.pprint(response.json())