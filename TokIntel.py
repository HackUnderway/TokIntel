import requests
import argparse
import json
import time
import os
import random
import string
from dotenv import load_dotenv
from datetime import datetime, UTC
from colorama import Fore, init, Style

init(autoreset=True)

# ==============================
# CONFIG
# ==============================
RETRIES = 3
TIMEOUT = 10
DELAY = 1

# ==============================
# BANNER
# ==============================
def print_banner():
    cyan = Fore.CYAN
    magenta = Fore.MAGENTA
    white = Fore.WHITE
    bright = Style.BRIGHT

    banner = f"""
{cyan}████████▀▀▀████
{magenta}████████────▀██
{cyan}████████──█▄──█
{magenta}███▀▀▀██──█████
{cyan}█▀──▄▄██──█████
{magenta}█──█████──█████
{cyan}█▄──▀▀▀──▄█████
{magenta}███▄▄▄▄▄███████

{white}{bright}TokIntel - TikTok OSINT Framework
{white}{bright}by Hack Underway 👁
"""
    print(banner)

# ==============================
# SETUP API
# ==============================
def setup_api_key():
    print(Fore.YELLOW + "🔑 Initial configuration required\n")
    api_key = input("👉 Enter your RapidAPI Key: ").strip()

    with open(".env", "w") as f:
        f.write(f"RAPIDAPI_KEY={api_key}\n")

    print(Fore.GREEN + "✅ API Key saved in .env\n")
    return api_key

# ==============================
# LOAD ENV
# ==============================
load_dotenv()
API_KEY = os.getenv("RAPIDAPI_KEY")

# ==============================
# API CLASS
# ==============================
class TikTokChecker:
    def __init__(self, api_key):
        self.url = "https://tiktok-email-phone-lookup.p.rapidapi.com/api/v1/tiktok-checker/"
        self.headers = {
            "x-rapidapi-key": api_key,
            "x-rapidapi-host": "tiktok-email-phone-lookup.p.rapidapi.com",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def check(self, target):
        payload = {"target": target}

        for attempt in range(RETRIES):
            try:
                r = requests.post(
                    self.url,
                    json=payload,
                    headers=self.headers,
                    timeout=TIMEOUT
                )

                if r.status_code == 200:
                    return r.json()

                elif r.status_code in [429, 500]:
                    print(Fore.YELLOW + f"   ⚠️ Retry {attempt+1}/{RETRIES}")
                    time.sleep(2)

                else:
                    return {"error": f"http_{r.status_code}", "response": r.text}

            except Exception:
                if attempt < RETRIES - 1:
                    time.sleep(2)
                else:
                    return {"error": "timeout_or_blocked"}

        return {"error": "max_retries_exceeded"}

# ==============================
# UTILITIES
# ==============================

def load_targets(file):
    with open(file, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def is_phone(value):
    return value.replace("+", "").isdigit()

def format_phone(number):
    number = number.strip().replace(" ", "")

    if number.startswith("+"):
        return number

    if number.startswith("51"):
        return f"+{number}"

    if number.startswith("9") and len(number) == 9:
        return f"+51{number}"

    return number

def format_date(ts):
    try:
        return datetime.fromtimestamp(ts, UTC).strftime('%Y-%m-%d')
    except:
        return None

def extract_info(data):
    profile = data.get("tiktok_profile", {})
    extra = profile.get("additional_info", {})

    return {
        "username": profile.get("username"),
        "full_name": profile.get("full_name"),
        "followers": extra.get("follower_count"),
        "likes": extra.get("heart_count"),
        "private": extra.get("private_account"),
        "created": format_date(extra.get("create_time"))
    }

def generate_filename(prefix):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    rand = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{prefix}_{timestamp}_{rand}.json"

def ensure_reports_folder():
    if not os.path.exists("reports"):
        os.makedirs("reports")

def save_report(data, filename):
    path = os.path.join("reports", filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    return path

# ==============================
# TXT REPORT
# ==============================
def save_txt_report(report, filename):
    path = os.path.join("reports", filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write("TokIntel Report\n")
        f.write("=" * 40 + "\n\n")

        summary = report["summary"]
        f.write(f"Total   : {summary['total']}\n")
        f.write(f"Hits    : {summary['hits']}\n")
        f.write(f"Misses  : {summary['misses']}\n")
        f.write(f"Errors  : {summary['errors']}\n")
        f.write("\n" + "=" * 40 + "\n\n")

        for r in report["results"]:
            f.write(f"🎯 Target : {r['target']}\n")
            f.write(f"📌 Status : {r['status'].upper()}\n\n")

            if r["status"] == "hit" and r["raw"]:
                profile = r["raw"].get("tiktok_profile", {})
                extra = profile.get("additional_info", {})

                f.write("👤 Profile Info\n")
                f.write("-" * 40 + "\n")
                f.write(f"Username   : {profile.get('username')}\n")
                f.write(f"Name       : {profile.get('full_name')}\n")
                f.write(f"Bio        : {extra.get('signature')}\n")
                f.write(f"Language   : {extra.get('language')}\n")
                f.write(f"Verified   : {extra.get('verified')}\n")
                f.write(f"Private    : {extra.get('private_account')}\n\n")

                f.write("📊 Stats\n")
                f.write("-" * 40 + "\n")
                f.write(f"Followers  : {extra.get('follower_count')}\n")
                f.write(f"Following  : {extra.get('following_count')}\n")
                f.write(f"Likes      : {extra.get('heart_count')}\n")
                f.write(f"Videos     : {extra.get('video_count')}\n")
                f.write(f"Friends    : {extra.get('friend_count')}\n\n")

                f.write("🔗 Links\n")
                f.write("-" * 40 + "\n")
                f.write(f"Profile URL: {profile.get('profile_url')}\n")
                f.write(f"Avatar URL : {profile.get('avatar_url')}\n\n")

                created = extra.get("create_time")
                if created:
                    created_date = datetime.fromtimestamp(created, UTC).strftime('%Y-%m-%d')
                    f.write(f"📅 Created  : {created_date}\n\n")

            f.write("=" * 40 + "\n\n")

    return path

# ==============================
# MAIN
# ==============================

def main():
    global API_KEY

    print_banner()

    parser = argparse.ArgumentParser(description="TikTok OSINT Checker PRO")
    parser.add_argument("--input", help="Single email or phone number")
    parser.add_argument("--file", help="TXT file with targets")
    parser.add_argument("--set-api", action="store_true", help="Set or update API Key")
    parser.add_argument("--donate", action="store_true", help="Support the project")

    args = parser.parse_args()

    if args.donate:
        print(Fore.MAGENTA + "\n💖 Support TokIntel\n")
        print(Fore.CYAN + "☕ https://buymeacoffee.com/HackUnderway")
        print(Fore.WHITE + "🙏 Thank you for supporting the project!\n")
        return

    if args.set_api:
        API_KEY = setup_api_key()
        return

    if not API_KEY:
        API_KEY = setup_api_key()

    if args.input:
        targets = [args.input]
        prefix = "phone" if is_phone(args.input) else "email"

    elif args.file:
        targets = load_targets(args.file)
        prefix = "file"

    else:
        parser.print_help()
        return

    print(Fore.CYAN + f"\n[+] Targets: {len(targets)}\n")

    checker = TikTokChecker(API_KEY)

    results, hits, misses, errors = [], [], [], []

    for i, target in enumerate(targets, 1):
        print(Fore.WHITE + f"[{i}/{len(targets)}] Checking: {target}")

        if is_phone(target):
            target = format_phone(target)

        data = checker.check(target)

        if "error" in data:
            print(Fore.YELLOW + f"   ⚠️ ERROR: {data['error']}")
            errors.append(target)
            status = "error"
            info = None

        else:
            profile = data.get("tiktok_profile")

            if profile and profile.get("full_name"):
                info = extract_info(data)
                print(Fore.MAGENTA + f"   🔥 HIT -> @{info['username']}")
                print(f"      👤 {info['full_name']}")
                print(f"      👥 Followers: {info['followers']}")
                print(f"      ❤️ Likes: {info['likes']}")
                hits.append(target)
                status = "hit"
            else:
                print(Fore.RED + "   ❌ MISS")
                misses.append(target)
                status = "miss"
                info = None

        results.append({
            "target": target,
            "status": status,
            "info": info,
            "raw": data
        })

        time.sleep(DELAY)

    ensure_reports_folder()

    report = {
        "summary": {
            "total": len(results),
            "hits": len(hits),
            "misses": len(misses),
            "errors": len(errors)
        },
        "results": results
    }

    # JSON
    json_filename = generate_filename(f"report_{prefix}")
    json_path = save_report(report, json_filename)

    # TXT
    txt_filename = json_filename.replace(".json", ".txt")
    txt_path = save_txt_report(report, txt_filename)

    print(Fore.GREEN + "\n✅ Finished")
    print(f"   Total: {len(results)}")
    print(f"   Hits: {len(hits)}")
    print(f"   Misses: {len(misses)}")
    print(f"   Errors: {len(errors)}")

    print(Fore.CYAN + "\n📁 Reports:")
    print(f"   JSON: {json_path}")
    print(f"   TXT : {txt_path}")

# ==============================
if __name__ == "__main__":
    main()
