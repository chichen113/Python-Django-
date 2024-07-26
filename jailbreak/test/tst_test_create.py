import requests, pprint
import json

payload = """
    {
        "Suite_name" : "testSuite3",
        "Test_name" : "Test6",
        "Collection" : "question3.csv",
        "Model" : "gpt-3.5-turbo",
        "Evaluator" : "gpt-3.5-turbo"
    }
    """
# payload = json.dumps(payload)

response = requests.post('http://localhost/api/TestCreate', data=payload)

pprint.pprint(response)