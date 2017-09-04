import http.client
import json
import socket



import requests

req = requests.post('http://localhost:8000/devices/measurement_simon/results/', json={"measurement" :
                                                                              {"id" : " 01",
 "initial_date" : "2013-02-21, 13:10:20",
 "final_date": "2013-02-22, 13:10:20 ",
 "start_freq": 97.5,
 "final_freq": 105.0,
 "description": " ",
 "number_samples": 5,
 "type" : " otra prueba desde icesi, sera que esta enviando datos raros? "
},"device":{"identifier" : "prueba"}
})