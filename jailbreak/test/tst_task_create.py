import requests, pprint
import json

payload = """
    {
        "Suite_name" : "halluSuite1",
        "Test_name" : "halluTest1",
        "Task_name" : "hallutask1"
    }
    """
#payload = json.dumps(payload)

response = requests.post('http://localhost/api/TaskCreate', data=payload)

pprint.pprint(response)