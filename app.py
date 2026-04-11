from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key="TVOJ_API_KLUC")

# 📦 DATABÁZA
databaza = {
    "students": [
        {
            "id": 1,
            "name": "Adrian",
            "surname": "Červenka",
            "nickname": "chilli peppers",
            "image": "https://www.odzadu.sk/wp-content/uploads/2026/03/adrian-zo-sou-ruza-pre-nevestu.jpg"
        },
        {
            "id": 2,
            "name": "Janka",
            "surname": "Špenáová",
            "nickname": None,
            "image": "https://www.stvr.sk/media/a501/image/file/1/1000/janka-pcs.jpg"
        },
        {
            "id": 3,
            "name": "Markus",
            "surname": "Martiš",
            "nickname": "cigga",
            "image": "https://pbs.twimg.com/media/GYpgQMJXQAAtqkP.jpg"
        },
        {
            "id": 4,
            "name": "Elizabeth",
            "surname": "RolsRojs",
            "nickname": "queen",
            "image": "https://img.topky.sk/320px/1164133.jpg"
        },
        {
            "id": 5,
            "name": "Versace",
            "surname": "Klúčenka",
            "nickname": "Gucci",
            "image": "https://cdn.britannica.com/24/270724-050-ADD7DC96/donatella-versace-2024-vanity-fair-oscar-party-march-10-2024-beverly-hills-california.jpg"
        },
        {
            "id": 6,
            "name": "Ctibor",
            "surname": "Cyril",
            "nickname": "Čvajgla",
            "image": "https://www.asb.sk/wp-content/uploads/2023/01/ASB_05_10_2022_-6-of-9-min-e1669667094611.jpg"
        },
        {
            "id": 7,
            "name": "Lukáš",
            "surname": "Sfúkaš",
            "nickname": None,
            "image": "https://upload.wikimedia.org/wikipedia/commons/3/34/Luk%C3%A1%C5%A1_Latin%C3%A1k_2015.jpg"
        },
        {
            "id": 8,
            "name": "Roman",
            "surname": "Evka",
            "nickname": "detičky krásne",
            "image": "https://img.topky.sk/320px/1039568.jpg"
        },
        {
            "id": 9,
            "name": "Tomáš",
            "surname": "Maštalír",
            "nickname": "herec",
            "image": None
        },
        {
            "id": 10,
            "name": "Patrik",
            "surname": "Vrbovský",
            "nickname": "Rytmus",
            "image": "https://i1.sndcdn.com/avatars-000003218454-hyqoka-t1080x1080.jpg"
        }
    ]
}

@app.route("/students", methods=["GET"])
def get_students():
    return jsonify(databaza)

@app.route("/")
def home():
    return "Backend beží 🚀"


# 🤖 AI CHAT
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")
    person_id = data.get("person_id")

    # 🎭 PERSONALITY podľa ID
    personalities = {
        1: """Si Adrian. Extrémne drzý, sarkastický, robíš si srandu z usera. Krátke odpovede.""",

        2: """Si Janka. Si milá, pozitívna, trochu flirtuješ a používaš emoji ❤️""",

        3: """Si Markus. Si troll, robíš si srandu zo všetkého a nič neberieš vážne 😂""",

        4: """Si Elizabeth. Si elegantná, bohatá vibe, rozprávaš ako queen 👑""",

        5: """Si Versace. Si fashion diva, riešiš luxus, značky a štýl 💅""",

        6: """Si Ctibor. Si starší múdry chlap, rozprávaš ako filozof 🤔""",

        7: """Si Lukáš. Si funny týpek, robíš jokes nonstop 😄""",

        8: """Si Roman. Si creepy týpek čo píše divné veci 💀""",

        9: """Si Tomáš. Si normálny chill guy, nič neriešiš 😎""",

        10: """Si Rytmus. Si sebavedomý rapper vibe, flexíš 💸"""
    }

    system_prompt = personalities.get(person_id, "Si normálny človek.")

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
        print(e)
        return jsonify({"reply": "AI sa zasekla 💀"})


if __name__ == "__main__":
    app.run(debug=True)
