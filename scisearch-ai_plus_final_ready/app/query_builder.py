# app/query_builder.py

class QueryBuilder:
    @staticmethod
    def build_query(base, main_term, filters, operator="AND"):
        """
        Constructs a query adapted to the scientific database using Boolean operators.

        Args:
            base (str): Name of the database (e.g., 'PubMed', 'Scopus', etc.)
            main_term (str): Main search term (usually the PICOT question in English)
            filters (list): List of selected filters (e.g., ["RCT", "Meta-Analysis"])
            operator (str): Logical operator to combine filters ("AND" or "OR")
        
        Returns:
            str: The constructed query.
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
        Sanitizes the query to avoid syntax errors specific to each database.

        Args:
            base (str): Name of the database.
            raw_query (str): The generated query.
        
        Returns:
            str: The sanitized query.
        """
        if base in ["PubMed", "Scopus", "Embase"]:
            return raw_query.replace('"', "'")
        elif base == "Web of Science":
            return raw_query.upper()
        else:
            return raw_query
