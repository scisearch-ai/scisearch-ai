# app/scopus_connector.py

import os
import re
import requests

def search_scopus(query: str, max_results: int = 20) -> list[dict]:
    """
    Realiza busca na base Scopus via API Elsevier.

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

    # Limpa '?' e espaços extras do final
    clean_query = re.sub(r"[?]+$", "", query).strip()

    base_url = "https://api.elsevier.com/content/search/scopus"
    headers = {
        "Accept":       "application/json",
        "X-ELS-APIKey": api_key
    }
    params = {
        "query": clean_query,
        "count": max_results
    }

    resp = requests.get(base_url, headers=headers, params=params)
    if resp.status_code != 200:
        raise Exception(f"Erro na requisição ao Scopus: {resp.status_code} - {resp.text}")

    data    = resp.json().get("search-results", {})
    entries = data.get("entry", [])

    articles = []
    for e in entries:
        if e.get("error"):
            continue
        title   = e.get("dc:title", "")
        # autores podem vir como string ou lista; aqui simplificamos:
        authors = [e["dc:creator"]] if isinstance(e.get("dc:creator"), str) else []
        journal = e.get("prism:publicationName", "")
        year    = e.get("prism:coverDate","").split("-")[0]
        # busca link “scopus”
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
