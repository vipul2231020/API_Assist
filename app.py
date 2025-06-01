from flask import Flask, request, jsonify
from gradio_client import Client
import re

# Gradio Space Client
client = Client("AIVipul/AI_Assist")

app = Flask(__name__)

def clean_reply(text):
    # Reference aur Context se related text hatao
    # Yeh regex "Reference(s):" ya "Context:" se shuru hone wali lines aur baad ke text hata dega
    # Agar aap aur strict chahte ho to is regex ko customize kar sakte ho
    cleaned = re.split(r"\nReference\(s\):|\nContext:", text)[0].strip()
    return cleaned

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message")
    history = data.get("history", [])

    if not message:
        return jsonify({"error": "Message is required"}), 400

    try:
        result = client.predict(
            message=message,
            chat_history_state=history,
            api_name="/respond"
        )
        # result expected: [chatbot_output, reply_text] (according to your earlier code)
        reply = result[1] if len(result) > 1 else ""
        cleaned_reply = clean_reply(reply)

        return jsonify({
            "reply": cleaned_reply,
            "chatbot_output": result[0]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
