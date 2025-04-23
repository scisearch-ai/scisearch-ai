# app/pubmed_connector.py

import os
import re
from Bio import Entrez

# Configurações do Entrez
Entrez.email   = os.environ.get("NCBI_EMAIL", "")
Entrez.api_key = os.environ.get("PUBMED_API_KEY", None)

def search_pubmed(query: str, max_results: int = 20) -> list[dict]:
    """
    Busca artigos no PubMed via E-Utilities (esearch + esummary).

    Retorna uma lista de dicionários com:
      - title   (str)
      - authors (list[str])
      - journal (str)
      - year    (str)
      - url     (str)
    """
    # Limpa '?' e espaços extras do final
    clean_query = re.sub(r"[?]+$", "", query).strip()

    # 1) ESearch (XML)
    handle = Entrez.esearch(
        db="pubmed",
        term=clean_query,
        retmax=max_results,
        api_key=Entrez.api_key
        # retmode XML é default
    )
    search_result = Entrez.read(handle)
    handle.close()

    id_list = search_result.get("IdList", [])
    if not id_list:
        return []

    # 2) ESummary (XML)
    handle = Entrez.esummary(
        db="pubmed",
        id=",".join(id_list),
        api_key=Entrez.api_key
    )
    summary = Entrez.read(handle)
    handle.close()

    records = summary.get("result", {})
    uids    = records.get("uids", [])

    articles = []
    for uid in uids:
        rec = records.get(uid, {})
        articles.append({
            "title":   rec.get("title", ""),
            "authors": [a.get("name", "") for a in rec.get("authors", [])],
            "journal": rec.get("fulljournalname", ""),
            "year":    (rec.get("pubdate","")[:4] if rec.get("pubdate") else ""),
            "url":     f"https://pubmed.ncbi.nlm.nih.gov/{uid}/"
        })

    return articles
