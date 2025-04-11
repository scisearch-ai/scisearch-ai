from flask import Blueprint, render_template, request, jsonify
from .pico_analyzer import analyze_question
from .evidence_fetcher import fetch_pubmed_data, fetch_scopus_data

app = Blueprint('app', __name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        question = data.get('question', '')
        time_filter = data.get('time_filter', '')
        study_types = data.get('study_types', [])

        if not question:
            return jsonify({'error': 'No question provided'}), 400

        pico_data = analyze_question(question)
        pubmed_results = fetch_pubmed_data(pico_data, time_filter, study_types)
        scopus_results = fetch_scopus_data(pico_data, time_filter, study_types)

        return jsonify({
            'pico': pico_data,
            'pubmed_results': pubmed_results,
            'scopus_results': scopus_results
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
