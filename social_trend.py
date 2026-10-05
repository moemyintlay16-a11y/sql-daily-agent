import os
import requests
from google import genai

# Secrets retrieved from GitHub Environment
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# Initialize Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)

# Prompt for bilingual social media trends
prompt = """
Search the web for the top global social media trends and viral topics right now.
Provide a concise summary in both English and Burmese (မြန်မာဘာသာဖြင့်ပါ တွဲ၍ဖော်ပြပါ).
Keep the format clean with emojis, bullet points, and clear separation between English and Burmese sections.
"""

# Generate content using Gemini 2.0 Flash
response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt
)

trend_text = response.text

# Send message to Telegram
telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
payload = {
    "chat_id": TELEGRAM_CHAT_ID,
    "text": trend_text
}

tg_response = requests.post(telegram_url, json=payload)

if tg_response.status_code == 200:
    print("Successfully sent bilingual trends to Telegram!")
else:
    print(f"Failed to send message. Telegram response: {tg_response.text}")
    exit(1)
