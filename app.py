from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# AVRAM Prototype Frontend Template with brand styling
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AVRAM — Ancient Wisdom. A Companion for Life.</title>
    <style>
        :root {
            --olive: #39483B;
            --parchment: #F3E9D5;
            --gold: #B89352;
            --charcoal: #252B29;
            --sandstone: #C8A77A;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--parchment);
            color: var(--charcoal);
            max-width: 680px;
            margin: 30px auto;
            padding: 20px;
            border-radius: 8px;
        }
        header {
            text-align: center;
            border-bottom: 2px solid var(--gold);
            padding-bottom: 15px;
            margin-bottom: 20px;
        }
        h1 { margin: 0; font-size: 1.8rem; color: var(--olive); letter-spacing: 0.5px; }
        p.tagline { margin: 5px 0 0; font-style: italic; color: #555; font-size: 0.95rem; }

        #chat-box {
            background: #ffffff;
            height: 380px;
            border: 1px solid var(--sandstone);
            overflow-y: scroll;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 6px;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
        }
        .message { margin-bottom: 15px; line-height: 1.4; }
        .user-msg { text-align: right; color: #2c3e50; }
        .user-msg span { background: #e2e8f0; padding: 8px 12px; border-radius: 8px; display: inline-block; text-align: left; }

        .avram-msg { text-align: left; color: var(--charcoal); }
        .avram-msg span { background: #fdfbf7; border-left: 3px solid var(--olive); padding: 10px 14px; border-radius: 0 8px 8px 0; display: inline-block; }

        .input-group { display: flex; gap: 10px; }
        input[type="text"] {
            flex-grow: 1;
            padding: 12px;
            border: 1px solid var(--sandstone);
            border-radius: 6px;
            font-size: 1rem;
            outline: none;
        }
        input[type="text"]:focus { border-color: var(--olive); }
        button {
            background-color: var(--olive);
            color: white;
            border: none;
            padding: 0 20px;
            border-radius: 6px;
            font-size: 1rem;
            cursor: pointer;
            transition: background 0.2s;
        }
        button:hover { background-color: #2c362b; }
        footer { text-align: center; font-size: 0.8rem; color: #777; margin-top: 20px; }
    </style>
</head>
<body>

    <header>
        <h1>AVRAM</h1>
        <p class="tagline">Ancient Wisdom. A Companion for Life.</p>
    </header>

    <div id="chat-box">
        <div class="message avram-msg">
            <span>Shalom. What is on your heart today? We can explore the Scriptures together, reflect on what you're facing, or walk the ancient paths.</span>
        </div>
    </div>

    <div class="input-group">
        <input type="text" id="user-input" placeholder="Ask a question or share what you're facing..." onkeypress="handleKey(event)">
        <button onclick="sendMessage()">Send</button>
    </div>

    <footer>
        AVRAM Prototype &bull; Grounded in Covenant & Scripture
    </footer>

    <script>
        async function sendMessage() {
            const input = document.getElementById('user-input');
            const chatBox = document.getElementById('chat-box');
            const text = input.value.trim();
            if (!text) return;

            // Append User Message
            chatBox.innerHTML += `<div class="message user-msg"><span>${escapeHtml(text)}</span></div>`;
            input.value = '';
            chatBox.scrollTop = chatBox.scrollHeight;

            // Send to Backend
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });
                const data = await response.json();

                // Append AVRAM Response
                chatBox.innerHTML += `<div class="message avram-msg"><span>${escapeHtml(data.reply)}</span></div>`;
                chatBox.scrollTop = chatBox.scrollHeight;
            } catch (err) {
                chatBox.innerHTML += `<div class="message avram-msg" style="color: red;"><span>Connection error. Please try again.</span></div>`;
            }
        }

        function handleKey(e) {
            if (e.key === 'Enter') sendMessage();
        }

        function escapeHtml(text) {
            return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
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
    user_message = data.get("message", "").strip()

    # Placeholder logic for prototype phase to reflect expected voice/tone guidelines
    if "forgive" in user_message.lower():
        reply = "Forgiveness can be difficult, especially when the hurt is deep. Would you like to explore what Scripture teaches about forgiveness, and how it differs from excusing wrongdoing or immediately restoring trust?"
    elif "sabbath" in user_message.lower():
        reply = "The Sabbath originates in the creation account and is established as a covenant sign. Christian traditions differ in how they understand observance today, focusing on its core purpose: rest, holiness, and remembrance."
    else:
        reply = f"Thank you for sharing that. In exploring '{user_message}', we look to Scripture to ground our understanding. How can we reflect on this together through wisdom (Chochmah) and understanding (Binah)?"

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)