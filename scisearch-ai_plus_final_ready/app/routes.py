# app/routes.py
from flask import Blueprint, render_template, request, jsonify
from app.pico_analyzer import analyze_question
from app.query_builder import QueryBuilder
from app.evidence_fetcher import fetch_pubmed_data, fetch_scopus_data
from app.triage_memory import load_memory, save_memory  # removido save_user_corrections
from app.triage_decorator import triage_article
from app.triage_interface import triage_bp  # Blueprint for Phase 7

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
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
        pico_result = analyze_question(question)
        return jsonify(pico_result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Se for usar correções manuais no futuro, reimplemente esta rota
# @bp.route('/save_picot_corrections', methods=['POST'])
# def save_picot_corrections():
#     ...

@bp.route('/results', methods=['POST'])
def results():
    data = request.get_json() or {}
    pico          = data.get('pico', {})
    selected_bases = data.get('bases', [])
    filters       = data.get('filters', {})
    operator      = data.get('operator', 'AND')
    year_range    = data.get('year_range')

    results_data = {}
    for base in selected_bases:
        q = QueryBuilder.build_query(
            base=base,
            main_term=pico.get("question_en", ""),
            filters=filters.get(base, []),
            operator=operator
        )
        q = QueryBuilder.sanitize_query(base, q)

        if base == "PubMed":
            results_data["PubMed"] = fetch_pubmed_data({"full_query": q}, year_range=year_range)
        elif base == "Scopus":
            results_data["Scopus"] = fetch_scopus_data({"full_query": q}, year_range=year_range)
        else:
            results_data[base] = {"error": "Base not implemented yet."}

    return jsonify({"results": results_data})

# Rota GET para servir a página de resultados
@bp.route('/results', methods=['GET'])
def results_page():
    # O JavaScript na página lerá localStorage e renderizará os dados
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

@bp.route('/triage', methods=['POST'])
def triage():
    data = request.get_json() or {}
    abstracts = data.get('abstracts', [])
    pico = data.get('pico', {})

    try:
        triage_results = [triage_article(abstract, pico) for abstract in abstracts]
        return jsonify({"triage": triage_results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Registrar blueprint de triagem avançada (fase 7)
bp.register_blueprint(triage_bp)
