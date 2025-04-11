from flask import Flask, render_template, request, jsonify
from app.pico_analyzer import analyze_question

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        question = data.get('question', '')
        if not question:
            return jsonify({"error": "Empty question"}), 400

        pico_result = analyze_question(question)
        return jsonify(pico_result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/results')
def results():
    # Esse é um placeholder para a página de resultados
    return "<h2>Resultados aparecerão aqui em breve!</h2>"
