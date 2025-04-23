# app/pubmed_connector.py

import os
from Bio import Entrez

# Configurações do Entrez
Entrez.email = os.environ.get("NCBI_EMAIL", "")
Entrez.api_key = os.environ.get("PUBMED_API_KEY", None)

def search_pubmed(query: str, api_key: str = None, max_results: int = 20) -> list[dict]:
    """
    Busca artigos no PubMed via E-Utilities (esearch + esummary).

    Retorna uma lista de dicionários com:
      - title   (str)
      - authors (list[str])
      - journal (str)
      - year    (str)
      - url     (str)
    """
    # 1) ESearch: pega os IDs
    handle = Entrez.esearch(
        db="pubmed",
        term=query,
        retmax=max_results,
        retmode="json",
        api_key=api_key or Entrez.api_key
    )
    res = Entrez.read(handle)
    handle.close()

    id_list = res.get("IdList", [])
    if not id_list:
        return []

    # 2) ESummary: obtém metadados de cada ID
    handle = Entrez.esummary(
        db="pubmed",
        id=",".join(id_list),
        retmode="json",
        api_key=api_key or Entrez.api_key
    )
    summary = Entrez.read(handle)
    handle.close()

    records = summary.get("result", {})
    uids = records.get("uids", [])

    articles = []
    for uid in uids:
        rec = records.get(uid, {})
        articles.append({
            "title": rec.get("title", ""),
            "authors": [ a.get("name","") for a in rec.get("authors", []) ],
            "journal": rec.get("fulljournalname", ""),
            "year":    (rec.get("pubdate","")[:4] if rec.get("pubdate") else ""),
            "url":     f"https://pubmed.ncbi.nlm.nih.gov/{uid}/"
        })

    return articles
