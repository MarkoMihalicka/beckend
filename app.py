from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

# 🔐 API KEY (lepšie cez env premennú)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "TVOJ_API_KLUC"))

# 📦 DATABÁZA (len pre /students endpoint)
databaza = {
    "students": [
        {"id": 1, "name": "Adrian", "surname": "Červenka", "nickname": "chilli peppers", "image": "https://www.odzadu.sk/wp-content/uploads/2026/03/adrian-zo-sou-ruza-pre-nevestu.jpg"},
        {"id": 2, "name": "Janka", "surname": "Špenáová", "nickname": None, "image": "https://www.stvr.sk/media/a501/image/file/1/1000/janka-pcs.jpg"},
        {"id": 3, "name": "Markus", "surname": "Martiš", "nickname": "cigga", "image": "https://pbs.twimg.com/media/GYpgQMJXQAAtqkP.jpg"},
        {"id": 4, "name": "Elizabeth", "surname": "RolsRojs", "nickname": "queen", "image": "https://img.topky.sk/320px/1164133.jpg"},
        {"id": 5, "name": "Versace", "surname": "Klúčenka", "nickname": "Gucci", "image": "https://cdn.britannica.com/24/270724-050-ADD7DC96/donatella-versace-2024-vanity-fair-oscar-party-march-10-2024-beverly-hills-california.jpg"},
        {"id": 6, "name": "Ctibor", "surname": "Cyril", "nickname": "Čvajgla", "image": "https://www.asb.sk/wp-content/uploads/2023/01/ASB_05_10_2022_-6-of-9-min-e1669667094611.jpg"},
        {"id": 7, "name": "Lukáš", "surname": "Sfúkaš", "nickname": None, "image": "https://upload.wikimedia.org/wikipedia/commons/3/34/Luk%C3%A1%C5%A1_Latin%C3%A1k_2015.jpg"},
        {"id": 8, "name": "Roman", "surname": "Evka", "nickname": "detičky krásne", "image": "https://img.topky.sk/320px/1039568.jpg"},
        {"id": 9, "name": "Tomáš", "surname": "Maštalír", "nickname": "herec", "image": None},
        {"id": 10, "name": "Patrik", "surname": "Vrbovský", "nickname": "Rytmus", "image": "https://i1.sndcdn.com/avatars-000003218454-hyqoka-t1080x1080.jpg"}
    ]
}

@app.route("/")
def home():
    return "Backend beží 🚀"

@app.route("/students", methods=["GET"])
def get_students():
    return jsonify(databaza)


# 🤖 AI CHAT
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    user_message = data.get("message")
    character = data.get("character")
    mood = data.get("mood", "neutral")

    if not character:
        return jsonify({"reply": "Chýba postava 💀"})

    # 🎭 POSTAVA
    name = character.get("name", "")
    surname = character.get("surname", "")
    personality = character.get("personality", "")
    style = character.get("style", "")
    moods = character.get("moods", {})

    mood_description = moods.get(mood, "normal")

    # 🧠 SYSTEM PROMPT (HLAVNÁ LOGIKA AI)
    system_prompt = f"""
You are {name} {surname}.

Personality: {personality}
Style: {style}
Current mood: {mood} ({mood_description})

You are chatting in a dating app called Markchat.

RULES:
- Speak like a real human
- Keep replies 1–2 sentences max
- Never say you are AI
- Stay in character ALWAYS
- Use emojis sometimes
- React naturally to user

MOOD BEHAVIOR:
- flirt → playful, more emojis, teasing
- friendly → open, talkative
- neutral → normal behavior
- nahnevana → cold, short, maybe rude
"""

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )

        reply = completion.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"reply": "AI sa zasekla 💀"})


if __name__ == "__main__":
    app.run(debug=True)
