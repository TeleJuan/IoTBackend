import requests
import json
url = "http://192.168.43.49:8080/api/device/switch"
#url = "http://192.168.43.49:8080/test"

params = {
    "state":1,
    "serial":"PLUG00"
}

x = requests.post(url,json=params)
#x = requests.get(url)