import os

import requests
from dotenv import load_dotenv

load_dotenv()

webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

if not webhook_url:
    raise ValueError("DISCORD_WEBHOOK_URL was not found in .env")

response = requests.post(
    webhook_url,
    json={"content": "Discord webhook is connected."},
    timeout=15,
)

if response.status_code == 204:
    print("Success! Test message sent to Discord.")
else:
    print("Discord returned status:", response.status_code)
    print("Response:", response.text)
