import http.client
import json
import socket
conn = http.client.HTTPConnection(socket.gethostname(),4573)

# data = {
# 	"Identificador": "json2",
# 	"FechaEjecucion": "2016-01-03 06:35:45",
# 	"Umbral": -80,
# 	"IdentificadorInstanciaAplicacion": "TESData 2",
# 	"MuestrasPorTrazo": 1,
# 	"Duracion": "00:03:00",
# 	"NumeroTrazos": 10,
# 	"DuracionPorBanda": 10000,
# 	"StartFreq": 90500000,
# 	"StopFreq": 106500000,
# 	"RefLevel": 5,
# 	"SweepTime": 0.0001,
# 	"ResBWidth": 14000,
# 	"VideoBWidth": 15000,
# 	"PowerAtt": 10,
# 	"ScalePDiv": 10,
# 	"Span": 16000000,
# }
#
# headers = {'Content-type': 'application/json'}
#
# mea = {'measurement': 'Hello world github/linguist#1 **cool**, and #1!'}
# json_mea = json.dumps(data)
#
# conn.request("GET", '/update', json.dumps(data), headers)
# r1 = conn.getresponse()
# print(r1.status, r1.reason)
#
# conn.close()
# import json
# import urllib.request
# req = urllib.request.urlopen('http://localhost:4573/index')
# req.add_header('Content-Type', 'application/json')
#
# response = urllib.request.Request(req, json.dumps(data))

import requests
req = requests.post('http://'+socket.gethostname()+':9000/json_in', json={'filter': 'calif'})