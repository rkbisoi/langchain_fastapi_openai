import json
import requests

url = "http://127.0.0.1:6677/stream_chat"
message = "Hello! How are you?"
data = {"content": message}


headers = {"Content-type": "application/json"}

with requests.post(url, data=json.dumps(data), headers=headers, stream=True) as r:
    for chunks in r.iter_content(102):
        print(chunks)


## Run this using command -->> python -m uvicorn main:app --reload --port 6677