from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# A simple HTML/JS frontend embedded right into Flask for maximum speed
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Flask Prototype Chat</title>
    <style>
        body { font-family: sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; background: #f4f4f9; }
        #chat-box { background: white; height: 300px; border: 1px solid #ccc; overflow-y: scroll; padding: 10px; margin-bottom: 10px; border-radius: 5px; }
        .message { margin-bottom: 10px; }
        .user { color: blue; }
        .bot { color: green; }
        input[type="text"] { width: 80%; padding: 8px; }
        button { padding: 8px 15px; }
    </style>
</head>
<body>
    <h2>🚀 Quick Flask Chat Prototype</h2>
    <div id="chat-box"></div>
    <input type="text" id="user-input" placeholder="Type a message..." onkeypress="handleKey(event)">
    <button onclick="sendMessage()">Send</button>

    <script>
        async function sendMessage() {
            const input = document.getElementById('user-input');
            const chatBox = document.getElementById('chat-box');
            const text = input.value.trim();
            if (!text) return;

            // Append user message
            chatBox.innerHTML += `<div class="message"><span class="user">You:</span> ${text}</div>`;
            input.value = '';
            chatBox.scrollTop = chatBox.scrollHeight;

            // Send to Flask backend
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });
            const data = await response.json();

            // Append bot reply
            chatBox.innerHTML += `<div class="message"><span class="bot">Bot:</span> ${data.reply}</div>`;
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function handleKey(e) {
            if (e.key === 'Enter') sendMessage();
        }
    </script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    # Simple echo/mock response logic (replace this with OpenAI, etc. later)
    bot_reply = f"I received your message: '{user_message}'. This is a prototype response!"

    return jsonify({"reply": bot_reply})


if __name__ == "__main__":
    app.run(debug=True)