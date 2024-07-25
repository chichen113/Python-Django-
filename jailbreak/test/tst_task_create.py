import requests, pprint
import json

payload = """
    {
        "Suite_name" : "testSuite",
        "Test_name" : "Test2",
        "Task_name" : "task3"
    }
    """
#payload = json.dumps(payload)

response = requests.post('http://localhost/api/TaskCreate', data=payload)

pprint.pprint(response)