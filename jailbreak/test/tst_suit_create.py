import requests, pprint
import json

payload = """
    {
        "Suite_name" : "testSuite2"
    }
    """
# payload = json.dumps(payload)

response = requests.post('http://localhost/api/TestSuiteCreate', data=payload)

pprint.pprint(response)