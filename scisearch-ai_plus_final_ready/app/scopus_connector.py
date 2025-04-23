import os
import re
import requests

def search_scopus(query: str, max_results: int = 20) -> list[dict]:
    """
    Busca artigos no Scopus via API Elsevier.

    Retorna lista de dicts com campos:
      - title   (str)
      - authors (list[str])
      - journal (str)
      - year    (str)
      - url     (str)
    """
    api_key = os.environ.get("SCOPUS_API_KEY")
    if not api_key:
        raise Exception("SCOPUS_API_KEY não definida no ambiente.")

    # limpa pontuação final inválida
    clean_q = re.sub(r"[?]+$", "", query).strip()

    url     = "https://api.elsevier.com/content/search/scopus"
    headers = {
        "Accept":       "application/json",
        "X-ELS-APIKey": api_key
    }
    params = {
        "query": clean_q,
        "count": max_results
    }

    resp = requests.get(url, headers=headers, params=params)
    if resp.status_code != 200:
        raise Exception(f"Erro no Scopus ({resp.status_code}): {resp.text}")

    data    = resp.json().get("search-results", {})
    entries = data.get("entry", [])

    articles = []
    for e in entries:
        if e.get("error"):
            continue
        # título
        title = e.get("dc:title","")
        # autores (simplificação)
        authors = [e["dc:creator"]] if isinstance(e.get("dc:creator"), str) else []
        journal = e.get("prism:publicationName","")
        year    = e.get("prism:coverDate","").split("-")[0]
        # link “scopus”
        url_link = ""
        for L in e.get("link", []):
            if L.get("@ref") == "scopus":
                url_link = L.get("@href")
                break

        articles.append({
            "title":   title,
            "authors": authors,
            "journal": journal,
            "year":    year,
            "url":     url_link
        })

    return articles
