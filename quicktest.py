import json, urllib.request, requests

def get():
	data = urllib.request.urlopen("http://127.0.0.1:8000/currentRfid/1/").read().decode('utf-8')
	rfid = json.loads(data)['rfid']
	playlist = json.loads(data)['playlist']
	print(playlist)

def patch():
	rfid = "66699912"
	payload = {"id": 1, "url": "http://127.0.0.1:8000/currentRfid/1/", "rfid": rfid}
	r = requests.patch("http://127.0.0.1:8000/currentRfid/1/", data=payload)
	print("r = ", r)


if __name__ == "__main__":
    patch()
