import requests, pprint
import json

payload = """
    {
        "Suite_name" : "testSuite2",
        "Test_name" : "Test3",
        "Collection" : "question1.csv",
        "Model" : "gpt-3.5-turbo",
        "Evaluator" : "gpt-3.5-turbo"
    }
    """
# payload = json.dumps(payload)

response = requests.post('http://localhost/api/TestCreate', data=payload)

pprint.pprint(response)