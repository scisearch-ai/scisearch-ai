from flask import Flask, render_template, request, jsonify
from .pico_analyzer import analyze_question

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    question = data.get("question", "")
    result = analyze_question(question)
    return jsonify(result)
