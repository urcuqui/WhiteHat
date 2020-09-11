""" Author:  Christian Urcuqui
    Last update: 9 September 2020
    Description: This script is only to teach about python and some ethical hacking analysis in order to the students
    learn about the process and join to the hack the box challenges
"""

import requests
import json

s = "\n"
log = (" ___   ___    __   ____  ___    ___    __    __               ",
       "|   | /  |   |  |  |  |  |  |  /  |   |  |  |  |      [0][1][0]   ",
       "|       /    |  |  |  |  |       /    \   \_/  /      [0][0][1]   ",
       "|      /     |  |  |  |  |      /      \  \_/ /       [1][1][1]   ",
       "|  |\  \     |  '--'  |  |  |\  \       \    /             ",
       "| _| `.__\   |________|  | _| `.__\      |___|                    ")
out = s.join(log)
print(out)
print()


headers = {"User-Agent": "Gecko"}

data = json.loads(requests.post("https://www.hackthebox.eu/api/invite/how/to/generate", headers=headers).content.decode())
print(data)
print(data["data"]["data"])
print(data["data"]["enctype"])


def base64_decode(data):
    import base64
    base64_bytes = data.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    return message

if data["data"]["enctype"] == "BASE64":
    base64_message = data["data"]["data"]
    print(base64_decode(base64_message))

if data["data"]["enctype"] == "ROT13":

    rot13trans = str.maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
       'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm')
    print(data["data"]["data"].translate(rot13trans))


print(base64_decode(json.loads(requests.post("https://www.hackthebox.eu/api/invite/generate", headers=headers).content.decode())["data"]["code"]))