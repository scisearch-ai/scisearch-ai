import os
import requests


def search_scopus(query: str, api_key: str = None, max_results: int = 20) -> dict:
    """
    Realiza uma busca na base Scopus usando a API da Elsevier.

    Parâmetros:
        - query (str): termo de busca (ex: 'diabetes AND exercise').
        - api_key (str, opcional): chave de API Scopus.
        - max_results (int): número máximo de resultados a serem retornados.

    Retorno:
        - dict: resposta da API contendo os dados dos artigos encontrados.
    """
    base_url = "https://api.elsevier.com/content/search/scopus"
    if not api_key:
        api_key = os.environ.get("SCOPUS_API_KEY")

    headers = {
        "Accept": "application/json",
        "X-ELS-APIKey": api_key
    }

    params = {
        "query": query,
        "count": max_results
    }

    response = requests.get(base_url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erro na requisição ao Scopus: {response.status_code} - {response.text}")
