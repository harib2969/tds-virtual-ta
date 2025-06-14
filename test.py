import requests

url = "https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34.json"
res = requests.get(url)
print(res.status_code)
print(res.json().keys())
