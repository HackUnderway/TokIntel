from apify_client import ApifyClient
import io
import contextlib
import argparse
import json
import time
import os
import random
import string
import sys
import warnings
import logging

# Suprimir TODOS los warnings y logs
warnings.filterwarnings('ignore')
os.environ['PYTHONWARNINGS'] = 'ignore'

# Silenciar logs de todas las librerías
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("apify_client").setLevel(logging.ERROR)
logging.getLogger("apify").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("requests").setLevel(logging.ERROR)
logging.getLogger("asyncio").setLevel(logging.ERROR)

from dotenv import load_dotenv
from datetime import datetime, UTC
from colorama import Fore, init, Style

init(autoreset=True)

RETRIES = 3
TIMEOUT = 30
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
# SPINNER ANIMADO (SIN THREADS)
# ==============================

def animated_spinner(seconds, message="🔍 Escaneando"):
    """Muestra un spinner animado por X segundos"""
    spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    start_time = time.time()
    i = 0
    
    while time.time() - start_time < seconds:
        elapsed = int(time.time() - start_time)
        spinner = spinner_chars[i % len(spinner_chars)]
        sys.stdout.write(f'\r{spinner} {message}... ({elapsed}s)')
        sys.stdout.flush()
        i += 1
        time.sleep(0.1)
    
    sys.stdout.write(f'\r✅ {message} completado ({seconds}s)   \n')
    sys.stdout.flush()


# ==============================
# API SETUP
# ==============================

def setup_api_key():
    print(Fore.YELLOW + "🔑 Initial configuration required\n")
    api_key = input("👉 Enter your Apify API Token: ").strip()
    with open(".env", "w") as f:
        f.write(f"APIFY_TOKEN={api_key}\n")
    print(Fore.GREEN + "✅ APIFY_TOKEN saved in .env\n")
    return api_key


# ==============================
# ENV
# ==============================

load_dotenv()
API_KEY = os.getenv("APIFY_TOKEN")


# ==============================
# APIFY CLIENT SIN LOGS
# ==============================

class SuppressOutput:
    """Context manager para suprimir completamente stdout y stderr"""
    def __enter__(self):
        self.devnull = open(os.devnull, 'w')
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        sys.stdout = self.devnull
        sys.stderr = self.devnull
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr
        self.devnull.close()


class TikTokChecker:
    def __init__(self, api_key):
        self.client = ApifyClient(api_key)
    
    def check(self, username):
        """Ejecuta el scraper completamente en silencio"""
        try:
            run_input = {
                "profiles": [username],
                "profileScrapeSections": ["videos"],
                "profileSorting": "latest",
                "resultsPerPage": 1,
                "shouldDownloadVideos": False,
                "shouldDownloadCovers": False,
                "shouldDownloadAvatars": False
            }
            
            # Suprimir TODA la salida durante la ejecución del scraper
            with SuppressOutput():
                run = self.client.actor(
                    "clockworks/tiktok-profile-scraper"
                ).call(
                    run_input=run_input
                )
            
            dataset_id = run.default_dataset_id
            items = list(self.client.dataset(dataset_id).iterate_items())
            
            if not items:
                return {}
            
            item = items[0]
            author = item.get("authorMeta", {})
            
            return {
                "tiktok_profile": {
                    "username": author.get("name"),
                    "full_name": author.get("nickName"),
                    "profile_url": author.get("profileUrl"),
                    "avatar_url": author.get("avatar"),
                    "additional_info": {
                        "verified": author.get("verified"),
                        "signature": author.get("signature"),
                        "bio_link": author.get("bioLink"),
                        "private_account": author.get("privateAccount"),
                        "followers": author.get("fans"),
                        "following": author.get("following"),
                        "friends": author.get("friends"),
                        "likes": author.get("heart"),
                        "videos": author.get("video"),
                        "create_time": author.get("createTime")
                    }
                }
            }
            
        except Exception as e:
            return {"error": str(e)}


# ==============================
# HELPERS
# ==============================

def load_targets(file):
    with open(file, "r", encoding="utf-8") as f:
        return [line.strip().replace("@", "") for line in f if line.strip()]


def format_date(ts):
    try:
        return datetime.fromtimestamp(ts, UTC).strftime("%Y-%m-%d")
    except:
        return "Unknown"


def format_number(num):
    """Formatea números grandes con comas"""
    try:
        return f"{num:,}"
    except:
        return str(num)


def extract_info(data):
    profile = data.get("tiktok_profile", {})
    extra = profile.get("additional_info", {})
    return {
        "username": profile.get("username"),
        "full_name": profile.get("full_name"),
        "followers": extra.get("followers"),
        "likes": extra.get("likes"),
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


def save_txt_report(report, filename):
    path = os.path.join("reports", filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write("TokIntel Report\n")
        f.write("=" * 60 + "\n\n")
        
        summary = report["summary"]
        f.write(f"Total   : {summary['total']}\n")
        f.write(f"Hits    : {summary['hits']}\n")
        f.write(f"Misses  : {summary['misses']}\n")
        f.write(f"Errors  : {summary['errors']}\n\n")
        
        for r in report["results"]:
            f.write(f"🎯 Username : {r['target']}\n")
            f.write(f"📌 Status   : {r['status'].upper()}\n\n")
            
            if r["status"] == "hit" and r["raw"]:
                profile = r["raw"]["tiktok_profile"]
                extra = profile["additional_info"]
                
                f.write(f"Username    : {profile.get('username')}\n")
                f.write(f"Name        : {profile.get('full_name')}\n")
                f.write(f"Profile URL : {profile.get('profile_url')}\n")
                f.write(f"Avatar URL  : {profile.get('avatar_url')}\n")
                f.write(f"Verified    : {extra.get('verified')}\n")
                f.write(f"Private     : {extra.get('private_account')}\n")
                f.write(f"Followers   : {format_number(extra.get('followers'))}\n")
                f.write(f"Following   : {format_number(extra.get('following'))}\n")
                f.write(f"Friends     : {format_number(extra.get('friends'))}\n")
                f.write(f"Likes       : {format_number(extra.get('likes'))}\n")
                f.write(f"Videos      : {format_number(extra.get('videos'))}\n")
                f.write(f"Created     : {format_date(extra.get('create_time'))}\n")
                f.write(f"Bio         : {extra.get('signature')}\n")
                f.write(f"Bio Link    : {extra.get('bio_link')}\n")
                f.write("\n")
            
            f.write("=" * 60 + "\n\n")
    return path


# ==============================
# MAIN
# ==============================

def main():
    global API_KEY
    
    print_banner()
    
    parser = argparse.ArgumentParser(description="TikTok OSINT Framework")
    parser.add_argument("--user", help="Single TikTok username")
    parser.add_argument("--users-file", help="TXT file with usernames")
    parser.add_argument("--set-api", action="store_true")
    parser.add_argument("--donate", action="store_true", help="Support the project")
    parser.add_argument("--show-avatar", action="store_true", help="Show avatar URL in console")
    
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
    
    if args.user:
        targets = [args.user.replace("@", "")]
        prefix = "user"
    elif args.users_file:
        targets = load_targets(args.users_file)
        prefix = "users"
    else:
        parser.print_help()
        return
    
    print(Fore.CYAN + f"\n[+] Targets: {len(targets)}\n")
    
    checker = TikTokChecker(API_KEY)
    
    results = []
    hits = []
    misses = []
    errors = []
    
    # Escanear cada objetivo
    for i, target in enumerate(targets, 1):
        print(Fore.WHITE + f"\n📌 [{i}/{len(targets)}] Escaneando: @{target}")
        print(Fore.YELLOW + "⏳ Iniciando conexión con Apify...")
        
        # Mostrar mensaje de inicio
        sys.stdout.write("🔄 Procesando solicitud...")
        sys.stdout.flush()
        
        start_time = time.time()
        
        # Ejecutar scraper (esto toma tiempo real)
        data = checker.check(target)
        
        elapsed = time.time() - start_time
        
        # Limpiar línea y mostrar completado
        sys.stdout.write(f'\r✅ Escaneo completado en {elapsed:.1f} segundos    \n')
        sys.stdout.flush()
        
        # Procesar resultados
        if "error" in data:
            print(Fore.YELLOW + f"⚠️ Error: {data['error']}")
            status = "error"
            info = None
            errors.append(target)
        else:
            profile = data.get("tiktok_profile")
            if profile:
                info = extract_info(data)
                extra = profile["additional_info"]
                
                # Mostrar resultados completos
                print(Fore.GREEN + f"\n{'═' * 60}")
                print(Fore.CYAN + f" 📱 Username    : @{profile.get('username')}")
                print(Fore.CYAN + f" 👤 Name        : {profile.get('full_name')}")
                print(Fore.CYAN + f" 🔗 Profile URL : {profile.get('profile_url')}")
                
                if args.show_avatar and profile.get('avatar_url'):
                    # Mostrar avatar completo si se pide
                    print(Fore.CYAN + f" 🖼️  Avatar URL  : {profile.get('avatar_url')}")
                
                print(Fore.CYAN + f" ✓ Verified     : {extra.get('verified')}")
                print(Fore.CYAN + f" 🔒 Private     : {extra.get('private_account')}")
                print(Fore.CYAN + f" 👥 Followers   : {format_number(extra.get('followers'))}")
                print(Fore.CYAN + f" 🔄 Following   : {format_number(extra.get('following'))}")
                print(Fore.CYAN + f" 👫 Friends     : {format_number(extra.get('friends'))}")
                print(Fore.CYAN + f" ❤️  Likes       : {format_number(extra.get('likes'))}")
                print(Fore.CYAN + f" 📹 Videos      : {format_number(extra.get('videos'))}")
                print(Fore.CYAN + f" 📅 Created     : {format_date(extra.get('create_time'))}")
                
                if extra.get('signature'):
                    print(Fore.CYAN + f" 📝 Bio         : {extra.get('signature')}")
                
                if extra.get('bio_link'):
                    print(Fore.CYAN + f" 🔗 Bio Link    : {extra.get('bio_link')}")
                
                print(Fore.GREEN + f"{'═' * 60}\n")
                
                hits.append(target)
                status = "hit"
            else:
                print(Fore.RED + f"\n❌ No se encontró información para @{target}\n")
                misses.append(target)
                status = "miss"
                info = None
        
        results.append({
            "target": target,
            "status": status,
            "info": info,
            "raw": data
        })
        
        if i < len(targets):
            time.sleep(DELAY)
    
    # Guardar reportes
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
    
    json_file = generate_filename(f"report_{prefix}")
    json_path = save_report(report, json_file)
    txt_path = save_txt_report(report, json_file.replace(".json", ".txt"))
    
    print(Fore.GREEN + "\n✅ Scan Finished\n")
    print(Fore.WHITE + f" Targets : {len(results)}")
    print(Fore.GREEN + f" Hits    : {len(hits)}")
    print(Fore.RED + f" Misses  : {len(misses)}")
    print(Fore.YELLOW + f" Errors  : {len(errors)}")
    print(Fore.CYAN + "\n📁 Reports")
    print(Fore.WHITE + f" JSON : {json_path}")
    print(Fore.WHITE + f" TXT  : {txt_path}\n")
    
    if not args.show_avatar:
        print(Fore.YELLOW + "💡 Tip: Usa --show-avatar para ver la URL completa del avatar en consola\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n⚠️ Escaneo interrumpido\n")
        sys.exit(0)