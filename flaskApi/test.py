import requests

BASE = "http://127.0.0.1:5000/"

response = requests.put(BASE + "video/3", {"name": "How to cook mayo 4", "views": 8, "likes": 7})
print(response.json())

response = requests.patch(BASE + "video/1", {"name": "How to cook mayo v2"})
print(response.json())

