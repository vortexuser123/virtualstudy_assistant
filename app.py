import os, json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
NOTES = "notes.txt"

def ask(prompt):
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"system","content":"Tutor who explains simply."},
                  {"role":"user","content":prompt}]
    )
    return r.choices[0].message.content.strip()

@app.post("/summarize")
def summarize():
    text = request.json.get("text","")
    return jsonify({"summary": ask(f"Summarize simply:\n{text}")})

@app.post("/flashcards")
def flashcards():
    topic = request.json.get("topic","")
    cards = ask(f"Make 8 concise flashcards (Q: A:) for {topic}. Use numbered list.")
    return jsonify({"flashcards": cards})

@app.post("/save-note")
def save_note():
    with open(NOTES,"a") as f: f.write(request.json.get("text","")+"\n")
    return {"ok":True}

@app.get("/notes")
def get_notes():
    return {"text": open(NOTES).read() if os.path.exists(NOTES) else ""}
    
if __name__ == "__main__":
    app.run(port=5051)
