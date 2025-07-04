import requests

url = "https://py.mit.edu/spring25/practice/diagram1"
response = requests.get(url)

with open("diagram1.html", "w", encoding="utf-8") as f:
    f.write(response.text)
