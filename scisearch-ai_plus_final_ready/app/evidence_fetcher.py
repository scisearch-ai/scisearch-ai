# app/evidence_fetcher.py

from .pubmed_connector import search_pubmed
from .scopus_connector import search_scopus

def fetch_pubmed_data(pico):
    """
    Recebe pico = {"full_query": "..."} e faz a chamada ao PubMed.
    """
    try:
        query = pico.get("full_query", "")
        return search_pubmed(query)
    except Exception as e:
        return {"error": f"PubMed fetch failed: {str(e)}"}

def fetch_scopus_data(pico):
    """
    Recebe pico = {"full_query": "..."} e faz a chamada ao Scopus.
    """
    try:
        query = pico.get("full_query", "")
        return search_scopus(query)
    except Exception as e:
        return {"error": f"Scopus fetch failed: {str(e)}"}
