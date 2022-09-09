import requests

response = requests.get("http://localhost:5000/sdwaterquality")
out = response.json()["water"]


for key in out[0]:
	print(key + ': ' + out[0][key])