import os
import re
from Bio import Entrez

# configurações do Entrez (é obrigatório setar NCBI_EMAIL no env)
Entrez.email   = os.environ.get("NCBI_EMAIL", "")
Entrez.api_key = os.environ.get("PUBMED_API_KEY", None)

def search_pubmed(query: str, max_results: int = 20) -> list[dict]:
    """
    Busca artigos no PubMed via E-Utilities (esearch + esummary).

    Retorna lista de dicts com campos:
      - title   (str)
      - authors (list[str])
      - journal (str)
      - year    (str)
      - url     (str)
    """
    # limpa pontuação final inválida
    clean_q = re.sub(r"[?]+$", "", query).strip()
    # 1) ESearch
    handle = Entrez.esearch(
        db="pubmed",
        term=clean_q,
        retmax=max_results,
        api_key=Entrez.api_key
    )
    search_res = Entrez.read(handle)
    handle.close()

    ids = search_res.get("IdList", [])
    if not ids:
        return []

    # 2) ESummary
    handle = Entrez.esummary(
        db="pubmed",
        id=",".join(ids),
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
            "authors": [a.get("name","") for a in rec.get("authors", [])],
            "journal": rec.get("fulljournalname",""),
            "year":    (rec.get("pubdate","")[:4] if rec.get("pubdate") else ""),
            "url":     f"https://pubmed.ncbi.nlm.nih.gov/{uid}/"
        })
    return articles

