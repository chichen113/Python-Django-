import requests, pprint
import json

payload = """
        {
            "Task_name": "task1"
        }
    """
# payload = json.dumps(payload)

response = requests.post('http://localhost/api/TaskExec', data=payload)

pprint.pprint(response)