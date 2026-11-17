import os, hashlib, requests
from bs4 import BeautifulSoup

URL = os.environ["WATCH_URL"]
TOKEN = os.environ["BOT_TOKEN"]
CHAT = os.environ["CHAT_ID"]
STATE = "last_hash.txt"

r = requests.get(URL, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(r.text, "html.parser")
# To watch only part of the page, uncomment and edit:
# soup = soup.select_one("#price")
text = soup.get_text(separator=" ", strip=True)
current = hashlib.md5(text.encode()).hexdigest()

last = open(STATE).read().strip() if os.path.exists(STATE) else None

if last is None:
    print("First run, saving baseline")
elif current != last:
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT, "text": f"Page changed: {URL}"},
        timeout=10,
    )

open(STATE, "w").write(current)
