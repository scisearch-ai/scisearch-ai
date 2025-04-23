# app/scopus_connector.py

import os
import requests

def search_scopus(query: str, max_results: int = 20) -> list[dict]:
    """
    Realiza uma busca na base Scopus usando a API da Elsevier.

    Retorna uma lista de dicionários com:
      - title   (str)
      - authors (list[str])
      - journal (str)
      - year    (str)
      - url     (str)
    """
    api_key = os.environ.get("SCOPUS_API_KEY")
    if not api_key:
        raise Exception("SCOPUS_API_KEY não definida no ambiente.")

    base_url = "https://api.elsevier.com/content/search/scopus"
    headers = {
        "Accept":       "application/json",
        "X-ELS-APIKey": api_key
    }
    params = {
        "query": query,
        "count": max_results
    }

    resp = requests.get(base_url, headers=headers, params=params)
    if resp.status_code != 200:
        raise Exception(f"Erro na requisição ao Scopus: {resp.status_code} - {resp.text}")

    data    = resp.json().get("search-results", {})
    entries = data.get("entry", [])

    articles = []
    for e in entries:
        # alguns registros podem já trazer erro embutido
        if e.get("error"):
            continue
        # título
        title = e.get("dc:title", "")
        # autores (pode vir como str ou não existir)
        authors = [e.get("dc:creator")] if isinstance(e.get("dc:creator"), str) else []
        # nome da revista
        journal = e.get("prism:publicationName", "")
        # ano de publicação
        year = e.get("prism:coverDate", "").split("-")[0]
        # link principal
        url = ""
        for link in e.get("link", []):
            if link.get("@ref") == "scopus":
                url = link.get("@href")
                break

        articles.append({
            "title":   title,
            "authors": authors,
            "journal": journal,
            "year":    year,
            "url":     url
        })

    return articles
