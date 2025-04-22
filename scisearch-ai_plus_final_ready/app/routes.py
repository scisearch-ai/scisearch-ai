# app/routes.py

from flask import Blueprint, render_template, request, jsonify
from app.pico_analyzer import analyze_question
from app.query_builder import QueryBuilder
from app.evidence_fetcher import fetch_pubmed_data, fetch_scopus_data
from app.triage_interface import triage_bp  # blueprint com /triage

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    # Passa o FILTER_OPTIONS para o template, para que o JS possa montar os checkboxes de filtros
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
            "DOCTYPE(ed)"   # Editorial
        ],
    }
    return render_template('index.html', filter_options=FILTER_OPTIONS)

@bp.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json() or {}
    question = data.get('question', '').strip()
    if not question:
        return jsonify({"error": "Empty question"}), 400

    try:
        pico = analyze_question(question)
        return jsonify(pico)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/results', methods=['POST'])
def results_api():
    """
    Endpoint que monta a query em cada base e retorna JSON
    """
    data = request.get_json() or {}
    pico           = data.get('pico', {})
    selected_bases = data.get('bases', [])
    filters        = data.get('filters', {})
    operator       = data.get('operator', 'AND')
    year_range     = data.get('year_range')

    if not pico or not selected_bases:
        return jsonify({"error": "Missing PICO or no databases selected"}), 400

    results_data = {}
    for base in selected_bases:
        raw_q = QueryBuilder.build_query(
            base=base,
            main_term=pico.get("question_en", ""),
            filters=filters.get(base, []),
            operator=operator
        )
        q = QueryBuilder.sanitize_query(base, raw_q)

        if base == "PubMed":
            results_data["PubMed"] = fetch_pubmed_data({"full_query": q}, year_range=year_range)
        elif base == "Scopus":
            results_data["Scopus"] = fetch_scopus_data({"full_query": q}, year_range=year_range)
        else:
            results_data[base] = {"error": "Base not implemented yet."}

    return jsonify({"results": results_data})

@bp.route('/results', methods=['GET'])
def results_page():
    """
    Página que vai ler do localStorage o JSON retornado pelo POST /results
    e renderizar via JS.
    """
    return render_template('results.html')

@bp.route('/summary-review')
def summary_review():
    return render_template('summary_review.html')

@bp.route('/title-selection')
def title_selection():
    return render_template('title_selection.html')

@bp.route('/abstract-review')
def abstract_review():
    return render_template('abstract_review.html')

# Registra o blueprint que define /triage
bp.register_blueprint(triage_bp)
