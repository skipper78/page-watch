import os, requests
from bs4 import BeautifulSoup

URL = "https://store.google.com/in/product/google_fitbit_air?hl=en-IN"
PRODUCT = "fitbit air"
TOKEN = os.environ["BOT_TOKEN"]
CHAT = os.environ["CHAT_ID"]
STATE = "last_state.txt"


def tg(msg):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT, "text": msg, "disable_web_page_preview": "true"},
        timeout=15,
    )


r = requests.get(
    URL,
    timeout=30,
    headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
        "Accept-Language": "en-IN,en;q=0.9",
    },
)
r.raise_for_status()
soup = BeautifulSoup(r.text, "html.parser")

labels = []
for el in soup.select('[data-component-name="cta"]'):
    if PRODUCT in (el.get("aria-label") or "").lower():
        t = el.get_text(" ", strip=True)
        if t and t not in labels:
            labels.append(t)

if not labels:
    raise SystemExit("Main button not found - page layout may have changed")

current = " | ".join(labels)
last = open(STATE).read().strip() if os.path.exists(STATE) else None

if last is None:
    tg(f"Monitoring started for Fitbit Air.\nCurrent button: {current}\n{URL}")
elif current != last:
    tg(f"Fitbit Air page changed!\n\nEarlier ({last}) ----> Now ({current})\n\n{URL}")
else:
    print("No change:", current)

open(STATE, "w").write(current)
