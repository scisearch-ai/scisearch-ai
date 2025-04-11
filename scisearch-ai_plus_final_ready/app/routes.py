# Routes placfrom flask import Flask, render_template, request, jsonify
from .pico_analyzer import analyze_question
from .evidence_fetcher import fetch_evidence
from .classified_terms import classify_terms

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    try:
        data = request.get_json()
        question = data.get("question", "")
        study_types = data.get("study_types", [])
        time_filter = data.get("time_filter", "any")

        # Análise PICOT e classificação
        pico_result = analyze_question(question)
        classified = classify_terms(pico_result)

        # Buscar evidências
        results = fetch_evidence(classified, study_types, time_filter)

        response = {
            "pico": pico_result,
            "classified": classified,
            "results": results
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
eholder
