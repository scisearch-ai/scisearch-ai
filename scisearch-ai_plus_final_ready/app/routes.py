@bp.route('/results', methods=['POST'])
def results_api():
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

        try:
            if base == "PubMed":
                # aqui, provisoriamente, forçamos uma string
                results_data["PubMed"] = fetch_pubmed_data(q, year_range=year_range)
            elif base == "Scopus":
                results_data["Scopus"] = fetch_scopus_data(q, year_range=year_range)
            else:
                results_data[base] = {"error": "Base not implemented yet."}
        except Exception as e:
            results_data[base] = {"error": f"{base} fetch failed: {str(e)}"}

    return jsonify({"results": results_data})
