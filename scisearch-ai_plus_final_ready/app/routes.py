# app/routes.py

from flask import Blueprint, render_template, request, jsonify
from app.pico_analyzer import analyze_question
from app.query_builder import QueryBuilder
from app.evidence_fetcher import fetch_pubmed_data, fetch_scopus_data
from app.triage_interface import triage_bp  # blueprint com /triage

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    # Passa as opções de filtro para o template via Jinja
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
    Recebe o JSON do client, constrói a query para cada base,
    chama o fetcher passando APENAS a query e o year_range,
    e devolve todos os resultados em JSON.
    """
    data = request.get_json() or {}
    pico           = data.get('pico', {})
    selected_bases = data.get('bases', [])
    filters        = data.get('filters', {})
    operator       = data.get('operator', 'AND')
    year_range     = data.get('year_range') or None

    if not pico or not selected_bases:
        return jsonify({"error": "Missing PICO or no databases selected"}), 400

    results_data = {}
    for base in selected_bases:
        # 1) gera e sanitiza a string de busca
        raw_q = QueryBuilder.build_query(
            base=base,
            main_term=pico.get("question_en", ""),
            filters=filters.get(base, []),
            operator=operator
        )
        q = QueryBuilder.sanitize_query(base, raw_q)

        # 2) chama o fetcher correspondente
        try:
            if base == "PubMed":
                # Note que agora passamos só (q, year_range)
                res = fetch_pubmed_data(q, year_range)
            elif base == "Scopus":
                res = fetch_scopus_data(q, year_range)
            else:
                res = {"error": "Base not implemented yet."}
        except Exception as e:
            res = {"error": f"{base} fetch failed: {str(e)}"}

        results_data[base] = res

    return jsonify({"results": results_data})

@bp.route('/results', methods=['GET'])
def results_page():
    # Simplesmente retorna o template: o JS vai ler do localStorage e renderizar tudo
    return render_template('results.html')

@bp.route('/summary-review')
def summary_review():
    return render_template('summary_review.html')

@bp.route('/title-selection')
def title_selection():
    return render_template('title_selection.html')

@bp.route('/abstract-review')
def abstract_review():
    return render_template('abstract-review.html')

# registra o blueprint de triagem (fase 7)
bp.register_blueprint(triage_bp)
