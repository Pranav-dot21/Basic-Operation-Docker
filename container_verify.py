import http.client
import json

conn = http.client.HTTPConnection('127.0.0.1', 5000)
body = json.dumps({"input1": 3, "input2": 4, "operator": "+"}).encode('utf-8')
conn.request('POST', '/calculate', body, {'Content-Type': 'application/json'})
r = conn.getresponse()
print(r.status)
print(r.read().decode())
