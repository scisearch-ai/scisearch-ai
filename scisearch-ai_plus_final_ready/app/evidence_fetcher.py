# app/evidence_fetcher.py

from .pubmed_connector import search_pubmed
from .scopus_connector import search_scopus

def fetch_pubmed_data(pico):
    """
    Chama o conector do PubMed passando apenas a query.
    Qualquer filtragem extra (ano, tipo de estudo) deve ser aplicada 
    dentro de search_pubmed, se suportado.
    """
    try:
        query = pico.get("full_query", "")
        return search_pubmed(query)
    except Exception as e:
        return {"error": f"PubMed fetch failed: {str(e)}"}

def fetch_scopus_data(pico):
    """
    Chama o conector do Scopus passando apenas a query.
    Qualquer filtragem extra (ano, tipo de estudo) deve ser aplicada 
    dentro de search_scopus, se suportado.
    """
    try:
        query = pico.get("full_query", "")
        return search_scopus(query)
    except Exception as e:
        return {"error": f"Scopus fetch failed: {str(e)}"}
