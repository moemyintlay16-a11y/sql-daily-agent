import json
import os
from google import genai
import requests

# ၁။ Environment Variables မှ Key များကို ယူခြင်း
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

HISTORY_FILE = "history.json"


# ၂။ မေးပြီးသား ခေါင်းစဉ် မှတ်တမ်းများကို ဖတ်ယူခြင်း
def load_history():
  if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
      return json.load(f)
  return []


def save_history(history):
  with open(HISTORY_FILE, "w", encoding="utf-8") as f:
    json.dump(history, f, indent=2, ensure_ascii=False)


# ၃။ Gemini API ဖြင့် လက်တွေ့သုံး SQL မေးခွန်း ထုတ်ယူခြင်း
def generate_sql_question(history):
  client = genai.Client(api_key=GEMINI_API_KEY)

  history_text = "\n".join([f"- {item}" for item in history[-30:]])

  prompt = f"""
You are a Principal Database Engineer. Generate ONE practical, real-world SQL challenge.

Guidelines:
- Base the question on realistic business logic (e.g., churn analysis, sessionization, inventory reconciliation).
- Focus on CTEs, Window Functions, self-joins, or complex aggregations.
- DO NOT repeat topics listed in Past Topics.

Past Topics:
{history_text if history_text else "None"}

Format Output using Telegram Markdown:
1. Business Context & Problem
2. Schema & Sample Data (DDL)
3. Expected Output
4. Difficulty Level (Medium/Hard)
"""

  response = client.models.generate_content(
      model="gemini-1.5-flash", contents=prompt
  )
  return response.text


# ၄။ Telegram သို့ မေးခွန်း ပေးပို့ခြင်း
def send_telegram_message(text):
  url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
  payload = {
      "chat_id": TELEGRAM_CHAT_ID,
      "text": text,
      "parse_mode": "Markdown",
  }
  requests.post(url, json=payload)


# ၅။ စတင် Run သည့် အပိုင်း
if __name__ == "__main__":
  history = load_history()
  question = generate_sql_question(history)
  send_telegram_message(question)

  # မေးပြီးသား ခေါင်းစဉ် အကျဉ်းချုပ်ကို မှတ်တမ်းထဲ ထည့်ခြင်း
  summary_prompt = (
      f"Extract a 5-word topic summary from this question:\n{question}"
  )
  client = genai.Client(api_key=GEMINI_API_KEY)
  summary_res = client.models.generate_content(
      model="gemini-2.5-flash", contents=summary_prompt
  )

  history.append(summary_res.text.strip())
  save_history(history)
