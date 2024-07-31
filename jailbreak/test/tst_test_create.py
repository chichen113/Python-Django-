import requests, pprint
import json

payload = """
    {
        "Suite_name" : "halluSuite1",
        "Test_name" : "halluTest1",
        "Collection" : "all_dataset.json",
        "Model" : "gpt-3.5-turbo",
        "Evaluator" : "gpt-3.5-turbo"
    }
    """
# payload = json.dumps(payload)

response = requests.post('http://localhost/api/TestCreate', data=payload)

pprint.pprint(response)