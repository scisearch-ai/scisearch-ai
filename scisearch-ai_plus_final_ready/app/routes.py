# app/routes.py
from flask import Blueprint, render_template, request, jsonify
from app.pico_analyzer import analyze_question
from app.query_builder import QueryBuilder
from app.evidence_fetcher import fetch_pubmed_data, fetch_scopus_data
from app.triage_memory import load_memory, save_memory
from app.triage_decorator import triage_article
from app.triage_interface import triage_bp  # Blueprint da fase 7, se necessário

# Crie um blueprint para as rotas deste módulo
bp = Blueprint('routes', __name__)

# Rota para a página inicial
@bp.route('/')
def index():
    # Defina aqui os filtros – o mesmo que você já tem
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
        # Adicione novas bases futuramente...
    }
    return render_template('index.html', filter_options=FILTER_OPTIONS)

# Rota para a análise automática da estrutura PICOT (Fase 1)
@bp.route('/analyze', methods=['POST'])
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

# Rota para a construção de queries (Fases 2 e 3)
@bp.route('/results', methods=['POST'])
def results():
    try:
        data = request.get_json()
        pico = data.get('pico', {})
        selected_bases = data.get('bases', [])
        filters = data.get('filters', {})
        operator = data.get('operator', 'AND')
        year_range = data.get('year_range')

        results_data = {}
        for base in selected_bases:
            query = QueryBuilder.build_query(
                base=base,
                main_term=pico.get("question_en", ""),
                filters=filters.get(base, []),
                operator=operator
            )
            query = QueryBuilder.sanitize_query(base, query)

            if base == "PubMed":
                results_data["PubMed"] = fetch_pubmed_data({"full_query": query}, year_range=year_range)
            elif base == "Scopus":
                results_data["Scopus"] = fetch_scopus_data({"full_query": query}, year_range=year_range)
            else:
                results_data[base] = {"error": "Base not implemented yet."}

        return jsonify({"results": results_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para a visualização por base (Fase 4)
@bp.route('/summary-review')
def summary_review():
    return render_template('summary_review.html')

# Rota para a seleção manual de títulos (Fase 5)
@bp.route('/title-selection')
def title_selection():
    return render_template('title_selection.html')

# Rota para a triagem por resumo (Fase 6)
@bp.route('/abstract-review')
def abstract_review():
    return render_template('abstract_review.html')

# Rota para a triagem automática com IA (Fase 7)
@bp.route('/triage', methods=['POST'])
def triage():
    try:
        data = request.get_json()
        abstracts = data.get('abstracts', [])
        pico = data.get('pico', {})

        triage_results = []
        for abstract in abstracts:
            decision = triage_article(abstract, pico)
            triage_results.append(decision)

        return jsonify({"triage": triage_results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Se você quiser incorporar também o blueprint da Fase 7 (se ele for definido em outro módulo)
bp.register_blueprint(triage_bp)

# Aliases para compatibilidade (se necessário)
load_memory = load_memory
save_memory = save_memory
