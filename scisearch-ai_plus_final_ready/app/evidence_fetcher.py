from .pubmed_connector import search_pubmed
from .scopus_connector import search_scopus

def fetch_pubmed_data(pico, time_filter=None, study_types=None):
    try:
        query = pico.get("full_query", "")
        return search_pubmed(query, study_types=study_types, year_range=time_filter)
    except Exception as e:
        return {"error": f"PubMed fetch failed: {str(e)}"}

def fetch_scopus_data(pico, time_filter=None, study_types=None):
    try:
        query = pico.get("full_query", "")
        return search_scopus(query, study_types=study_types, year_range=time_filter)
    except Exception as e:
        return {"error": f"Scopus fetch failed: {str(e)}"}
