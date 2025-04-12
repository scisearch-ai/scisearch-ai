# app/query_builder.py

class QueryBuilder:
    @staticmethod
    def build_query(base, main_term, filters, operator="AND"):
        """
        Constrói uma query adaptada à base científica com operadores booleanos.

        Args:
            base (str): Nome da base ('PubMed', 'Scopus', etc.)
            main_term (str): Termo principal de busca (normalmente a pergunta PICOT em inglês)
            filters (list): Lista de filtros selecionados (ex: ["RCT", "Meta-Analysis"])
            operator (str): Operador lógico para combinar filtros ("AND" ou "OR")
        """
        if not filters:
            return main_term

        if base == "PubMed":
            joined_filters = f" {operator} ".join(filters)
            return f"{main_term} AND ({joined_filters})" if len(filters) > 1 else f"{main_term} AND {filters[0]}"

        elif base == "Scopus":
            return f"{main_term} AND ({' OR '.join(filters)})"

        elif base == "Web of Science":
            return f"TS=({main_term}) AND DT=({' OR '.join(filters)})"

        elif base == "SciELO":
            return f"{main_term} AND {' AND '.join(filters)}"

        elif base == "Google Scholar":
            return f"{main_term} AND ({' OR '.join(filters)})"

        elif base == "Embase":
            return f"{main_term} AND ({' OR '.join(filters)})"

        elif base == "Cochrane":
            return f"{main_term} AND ({' OR '.join(filters)})"

        elif base == "LILACS":
            return f"{main_term} AND {' AND '.join(filters)}"

        elif base == "EBSCO":
            return f"{main_term} AND ({' OR '.join(filters)})"

        elif base == "PEDro":
            return f"{main_term} AND {' AND '.join(filters)}"

        else:
            return f"{main_term} {' '.join(f'{operator} {f}' for f in filters)}"

    @staticmethod
    def sanitize_query(base, raw_query):
        """
        Sanitiza a query para evitar erros de sintaxe específicos por base.

        Args:
            base (str): Nome da base
            raw_query (str): Query gerada
        """
        if base in ["PubMed", "Scopus", "Embase"]:
            return raw_query.replace('"', "'")
        elif base == "Web of Science":
            return raw_query.upper()
        else:
            return raw_query
