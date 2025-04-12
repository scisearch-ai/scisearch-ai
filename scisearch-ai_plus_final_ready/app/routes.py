from flask import Flask, render_template, request, jsonify
from app.pico_analyzer import analyze_question
from app.query_builder import QueryBuilder
from app.evidence_fetcher import fetch_pubmed_data, fetch_scopus_data

app = Flask(__name__)

# Filtros por tipo de estudo específicos por base
FILTER_OPTIONS = {
    "PubMed": [
        "Randomized Controlled Trial[Publication Type]",
        "Systematic Review[Publication Type]",
        "Meta-Analysis[Publication Type]",
        "Observational Study[Publication Type]",
        "Case Reports[Publication Type]"
    ],
    "Scopus": [
        "DOCTYPE(ar)",  # Article
        "DOCTYPE(re)",  # Review
        "DOCTYPE(cp)",  # Conference Paper
        "DOCTYPE(ch)",  # Book Chapter
        "DOCTYPE(ed)",  # Editorial
    ],
    # Futuras bases poderão ser adicionadas aqui...
}


@app.route('/')
def index():
    return render_template('index.html', filter_options=FILTER_OPTIONS)


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


@app.route('/results', methods=['POST'])
def results():
    try:
        data = request.get_json()
        pico = data.get('pico', {})
        selected_bases = data.get('bases', [])  # ["PubMed", "Scopus"]
        filters = data.get('filters', {})        # {"PubMed": [...], "Scopus": [...]}
        operator = data.get('operator', 'AND')   # Boolean operator: "AND" / "OR"
        year_range = data.get('year_range')      # Ex: "2015:2024"

        results = {}

        for base in selected_bases:
            query = QueryBuilder.build_query(
                base=base,
                main_term=pico.get("question_en", ""),
                filters=filters.get(base, []),
                operator=operator
            )
            query = QueryBuilder.sanitize_query(base, query)

            if base == "PubMed":
                results["PubMed"] = fetch_pubmed_data({"full_query": query}, year_range=year_range)
            elif base == "Scopus":
                results["Scopus"] = fetch_scopus_data({"full_query": query}, year_range=year_range)
            else:
                results[base] = {"error": "Base not implemented yet."}

        return jsonify({"results": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
