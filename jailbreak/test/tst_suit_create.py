import requests, pprint
import json

payload = """
    {
        "Suite_name" : "testSuite"
    }
    """
# payload = json.dumps(payload)

response = requests.post('http://localhost/api/TestSuiteCreate', data=payload)

pprint.pprint(response)