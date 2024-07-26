import requests, pprint
import json

payload = """
    {
        "Suite_name" : "testSuite2",
        "Test_name" : "Test4",
        "Task_name" : "task8"
    }
    """
#payload = json.dumps(payload)

response = requests.post('http://localhost/api/TaskCreate', data=payload)

pprint.pprint(response)