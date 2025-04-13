from flask import Flask, render_template, request, jsonify
from app.pico_analyzer import analyze_question
from app.query_builder import QueryBuilder
from app.evidence_fetcher import fetch_pubmed_data, fetch_scopus_data
from app.triage_memory import load_memory, save_memory
from app.triage_decorator import triage_article
from app.triage_interface import triage_bp  # ✅ NOVO: importa blueprint da Fase 7

app = Flask(__name__)
app.register_blueprint(triage_bp)  # ✅ NOVO: registra a Fase 7 com IA

# 🔎 Filtros específicos por base (usados no frontend dinâmico)
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
    # 🔜 Adicione novas bases aqui futuramente
}

# ✅ Página inicial com entrada da pergunta clínica
@app.route('/')
def index():
    return render_template('index.html', filter_options=FILTER_OPTIONS)

# ✅ Fase 1: Análise automática da estrutura PICOT
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

# ✅ Fase 2 e 3: Construção de queries + aplicação de filtros por base
@app.route('/results', methods=['POST'])
def results():
    try:
        data = request.get_json()
        pico = data.get('pico', {})
        selected_bases = data.get('bases', [])  # ["PubMed", "Scopus"]
        filters = data.get('filters', {})        # {"PubMed": [...], "Scopus": [...]}
        operator = data.get('operator', 'AND')   # "AND" / "OR"
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

# ✅ Fase 4: Visualização agrupada por base (quantidade de estudos e títulos)
@app.route('/summary-review')
def summary_review():
    return render_template('summary_review.html')

# ✅ Fase 5: Seleção manual de títulos com checkbox
@app.route('/title-selection')
def title_selection():
    return render_template('title_selection.html')

# ✅ Fase 6 (inicial): Triagem por resumo com inclusão/exclusão
@app.route('/abstract-review')
def abstract_review():
    return render_template('abstract_review.html')
