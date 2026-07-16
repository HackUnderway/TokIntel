<h1 align="center">TokIntel 👁</h1>

<p align="center">
  <strong>Advanced TikTok OSINT Framework</strong> to extract profiles, bios, creation dates, and full metadata from TikTok usernames 🕵🏽‍♂️
</p>

<p align="center">
  <img src="assets/TokIntel.png" title="TokIntel" alt="TokIntel" width="600"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white" alt="Python version">
  <img src="https://img.shields.io/badge/Apify-API-blue?logo=apify&logoColor=white">
  <img src="https://img.shields.io/badge/License-MIT-green?logo=open-source-initiative&logoColor=white" alt="License">
</p>

---

## 🚀 Features

- 🔎 **Profile Reconnaissance:** Extracts full TikTok profile data from usernames.
- 📊 **Rich Metadata Extraction:** Recovers creation dates, bios, full metrics (followers, likes, videos, friends, etc.), and high-res avatars.
- ⚡ **Fast API-Based Checking:** Powered by Apify's TikTok Profile Scraper.
- 📄 **JSON and TXT Report Generation:** Automatically saves all structured results locally.
- 🎨 **Colored CLI Interface:** Clean, aesthetic, and professional terminal output.
- 🔐 **Secure API Key Handling:** Credentials strictly managed via `.env`.
- 📂 **Batch Processing:** Scan lists of targets via TXT file.
- 💡 **Automatic API Setup:** Interactive onboarding on the first run.

## 📌 Prerequisites

- Python 3.8+
- Dependencies: `apify-client`, `python-dotenv`, `colorama`, `alive-progress`

# 🔑 API Key (Apify)

TokIntel uses the following API:

| NAME | KEY |
| ---- | --- |
| [TikTok Profile Scraper](https://apify.com/clockworks/tiktok-profile-scraper) | 🔑 (Required) |

### Steps:
1. Go to [Apify](https://apify.com) and create a free account.
2. Get your **API Token** from your Apify account settings.
3. Copy your API Token.

<p align="center">
  <img src="assets/TikTok_Profile_Scraper.png" title="TokIntel" alt="TokIntel" width="600"/>
</p>

<p align="center">
  <img src="assets/TikTok_Scraper.png" title="TokIntel" alt="TokIntel" width="600"/>
</p>

<p align="center">
  <img src="assets/Api_Tokens.png" title="TokIntel" alt="TokIntel" width="600"/>
</p>


# ⚙️ Configuration

The first time you run the tool, it will ask for your API key:

```bash
python3 TokIntel.py
```

Your key will be automatically saved in:

.env

<p align="center">
  <img src="assets/set_api.png" title="TokIntel" alt="TokIntel" width="600"/>
</p>

You can update it anytime:

```bash
python3 TokIntel.py --set-api
```

---

# 💻 Usage

### 🔹 Single target
```bash
python3 TokIntel.py --user jeyzetaoficial
```
```bash
python3 TokIntel.py --user jeyzetaoficial --show-avatar
```
```bash
python3 TokIntel.py --users-file targets.txt
```
`targets.txt should contain one username per line (without @).`
```bash
python3 TokIntel.py -h
```

<p align="center">
  <img src="assets/help_tokintel.png" title="TokIntel" alt="TokIntel" width="600"/>
</p>

---

# 📁 Reports

All results are saved in the `/reports/` directory.

Example file:
`report_email_20260328_xxxxxx.json`

> [!TIP]
> **Note:** Check the generated JSON report for advanced profile metadata not displayed in the terminal.

---

# 📦 Installation

```bash
git clone https://github.com/HackUnderway/TokIntel.git
```
```bash
cd TokIntel
```
```bash
pip install -r requirements.txt
```

> [!WARNING]
> ## Disclaimer
> This tool is intended for **educational and OSINT research purposes only**.
> - Do not use for illegal activities.
> - The developer is not responsible for any misuse or damage caused by this tool.

---

# 🧠 Notes

- Phone lookups may be unreliable due to API limitations
- Results depend on external data sources
- A "MISS" does not guarantee the account does not exist

> **The project is open to collaborators and partners.**

# 🧪 Supported Systems
|Distribution | Verified version | 	Supported | 	Status |
|--------------|--------------------|------|-------|
|Kali Linux| 2026.1| ✅| Working   |
|Parrot Security OS| 6.3| ✅ | Working   |
|Windows| 11 | ✅ | Working   |
|BackBox| 9 | ✅ | Working   |
|Arch Linux| 2024.12.01 | ✅ | Working   |

# Support
For questions, bug reports, or suggestions, please contact: info@hackunderway.com

# License
- [x] TokIntel is licensed.
- [x] See the [LICENSE](https://github.com/HackUnderway/TokIntel#MIT-1-ov-file) file for more information.

# 👨‍💻 Author

* [Victor Bancayan](https://www.offsec.com/bug-bounty-program/) - (**CEO at [Hack Underway](https://hackunderway.com/)**) 

## 🔗 Links
[![Patreon](https://img.shields.io/badge/patreon-000000?style=for-the-badge&logo=Patreon&logoColor=white)](https://www.patreon.com/c/HackUnderway)
[![Web site](https://img.shields.io/badge/Website-FF7139?style=for-the-badge&logo=firefox&logoColor=white)](https://hackunderway.com)
[![Facebook](https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white)](https://www.facebook.com/HackUnderway)
[![YouTube](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@JeyZetaOficial)
[![Twitter/X](https://img.shields.io/badge/Twitter/X-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/JeyZetaOficial)
[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://instagram.com/hackunderway)
[![TryHackMe](https://img.shields.io/badge/TryHackMe-212C42?style=for-the-badge&logo=tryhackme&logoColor=white)](https://tryhackme.com/p/JeyZeta)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-FF5E5B?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/hackunderway)
[![HackTheBox](https://img.shields.io/badge/HackTheBox-111927?style=for-the-badge&logo=hackthebox&logoColor=9FEF00)](https://profile.hackthebox.com/profile/019d59e8-fcc1-72e9-9aad-ff79f46d261d)

### 💰 Bitcoin Donations
Support the project with Bitcoin:

### Address:
```bash
bc1qjd5pu8kmdq1jun3qyw5e9mj4kdef9n8sutj7j4
```

<p align="center"> <img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=bc1qjd5pu8kmdq1jun3qyw5e9mj4kdef9n8sutj7j4" alt="Bitcoin QR"> </p>
Thank you for your support! 🙏

## ☕️ Support the project

If you like this tool, consider buying me a coffee:

[![Buy Me a Coffee](https://img.shields.io/badge/-Buy%20me%20a%20coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/hackunderway)

## 🌞 Subscriptions

###### Subscribe to: [Jey Zeta](https://www.facebook.com/JeyZetaOficial/subscribe/)

[![Kali Linux](https://img.shields.io/badge/Kali_Linux-557C94?style=for-the-badge&logo=kalilinux&logoColor=white)](https://www.kali.org/)

from <img src="https://i.imgur.com/ngJCbSI.png" title="Perú" width="20"/> Peru, made in <img src="https://i.imgur.com/NNfy2o6.png" title="Python" width="20"/> with <img src="https://i.imgur.com/S86RzPA.png" title="Love" width="20"/> by: Victor Bancayan

© 2026
