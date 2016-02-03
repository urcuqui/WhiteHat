import http.client
import json
import socket



import requests

req = requests.post('http://127.0.0.1:8080/measurement', json={"measurement" :
                                                                              {"id" : " 01",
 "initial_date" : "2013-02-21, 13:10:20",
 "final_date": "2013-02-22, 13:10:20 ",
 "start_freq": 97.5,
 "final_freq": 105.0,
 "description": " ",
 "number_samples": 5,
 "type" : " loc "
}
})
print(req.json())