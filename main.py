import os
import json
import requests
from google import genai

# Secrets retrieved from GitHub Environment
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# Load previous topics history
history_file = "history.json"
if os.path.exists(history_file):
    with open(history_file, "r") as f:
        history = json.load(f)
else:
    history = []

# Initialize Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)

prompt = f"""
Create a short, concise practical daily SQL question.
Avoid repeating these past topics: {json.dumps(history)}

Keep the format concise:
1. 🎯 Topic & Difficulty
2. 📋 Schema & Data
3. ❓ Question
4. 💡 Solution & Explanation
"""

# Generate SQL Question using Gemini 2.0 Flash
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=prompt
)

question_text = response.text

# Send message to Telegram
telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
payload = {
    "chat_id": TELEGRAM_CHAT_ID,
    "text": question_text
}

tg_response = requests.post(telegram_url, json=payload)

if tg_response.status_code == 200:
    print("Successfully sent message to Telegram!")
else:
    print(f"Failed to send message. Telegram response: {tg_response.text}")
    exit(1)

# Save history record
history.append("SQL Practice Problem")
with open(history_file, "w") as f:
    json.dump(history, f, indent=2)
