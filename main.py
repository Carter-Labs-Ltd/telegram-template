from flask import Flask, request, jsonify
import requests
import json

SERVER_URL = "YOUR SERVER'S PUBLIC URL (Must be HTTPS)"
TOKEN = "YOUR TELEGRAM BOT TOKEN"
CARTER_AGENT_KEY = "YOUR CARTER API KEY"
app = Flask(__name__)


def send_message(chat_id, text, telegram_key):
  """Sends a message to a Telegram chat."""
  url = f"https://api.telegram.org/bot{telegram_key}/sendMessage"
  payload = {"chat_id": chat_id, "text": text}
  response = requests.post(url, json=payload)
  response.raise_for_status(
  )  # Raise an exception if the request was unsuccessful
  return response.json()


def set_webhook(url, token):
  """Sets a webhook for a Telegram bot."""
  requests.post(
      f"https://api.telegram.org/bot{token}/deleteWebhook?drop_pending_updates=true"
  )

  tg_url = f"https://api.telegram.org/bot{token}/setWebhook?drop_pending_updates=true"
  response = requests.post(tg_url,
                           json={
                               "url": url,
                               "drop_pending_updates": True
                           })
  response.raise_for_status()
  return response.json()


def set_is_typing(chat_id, is_typing, telegram_key):
  """Sets the 'typing' status for a Telegram chat."""
  url = f"https://api.telegram.org/bot{telegram_key}/sendChatAction"
  payload = {
      "chat_id": chat_id,
      "action": "typing" if is_typing else "cancel_typing"
  }
  response = requests.post(url, json=payload)
  response.raise_for_status()
  return response.json()


def get_carter_response(input_text, user_id):
  """Fetches a response from the Carter Labs API."""
  response = requests.post(
      "https://api.carterlabs.ai/chat",
      headers={"Content-Type": "application/json"},
      data=json.dumps({
          "text": input_text,
          "key": CARTER_AGENT_KEY,
          "user_id": user_id,
          "context": "THIS CONVERSATION IS ON TELEGRAM",
      }),
  )
  response.raise_for_status()
  return response.json()["output"]["text"]


@app.route("/on-message", methods=["POST"])
def handle_message():
  """Handles incoming messages and responds accordingly."""
  data = request.json
  user_id = data["message"]["from"]["id"]

  if "text" not in data["message"]:
    send_message(user_id, "Please send text only", TOKEN)
    return jsonify({"success": False, "error": "Missing input content"})
  else:
    text = data["message"]["text"]

    if text is None:
      return jsonify({"success": False, "error": "Missing input content"})

    response = get_carter_response(text, user_id)
    response = send_message(user_id, response, TOKEN)
    return jsonify(response)


@app.route("/", methods=["GET"])
def index():
  return "Hello World!"


if __name__ == "__main__":
  set_webhook(SERVER_URL + "/on-message", TOKEN)
  app.run(threaded=True, port=5123, host="0.0.0.0")
