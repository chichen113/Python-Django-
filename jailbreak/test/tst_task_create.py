import requests, pprint
import json

payload = """
    {
        "Suite_name" : "testSuite",
        "Test_name" : "Test1",
        "Task_name" : "task2"
    }
    """
#payload = json.dumps(payload)

response = requests.post('http://localhost/api/TaskCreate', data=payload)

pprint.pprint(response)