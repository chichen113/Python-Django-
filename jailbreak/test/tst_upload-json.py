import requests
import pprint

# 文件路径
file_path = 'F:/Desktop/123/Python-Django-/jailbreak/api/all_dataset.json'

# 使用 files 参数上传文件
with open(file_path, 'rb') as file:
    files = {'file': file}
    response = requests.post('http://localhost/api/upload-json', files=files)

# 打印响应
pprint.pprint(response.json())
