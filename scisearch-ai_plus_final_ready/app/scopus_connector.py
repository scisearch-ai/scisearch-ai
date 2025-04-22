# app/scopus_connector.py

import os
import requests

def search_scopus(query: str, api_key: str = None, max_results: int = 20) -> dict:
    """
    Realiza uma busca na base Scopus usando a API da Elsevier.

    Parâmetros:
        - query (str): termo de busca (ex: 'diabetes AND exercise').
        - api_key (str, opcional): chave de API Scopus (caso não seja passada,
          é lida da variável de ambiente SCOPUS_API_KEY).
        - max_results (int): número máximo de resultados a serem retornados.

    Retorno:
        - dict: resposta bruta da API contendo os dados dos artigos encontrados.
    """
    # Obtém a chave de API, preferencialmente do parâmetro ou do env
    if not api_key:
        api_key = os.environ.get("SCOPUS_API_KEY")
    if not api_key:
        raise Exception("SCOPUS_API_KEY não definida no ambiente.")

    base_url = "https://api.elsevier.com/content/search/scopus"
    headers = {
        "Accept": "application/json",
        "X-ELS-APIKey": api_key
    }
    params = {
        "query": query,
        "count": max_results
    }

    response = requests.get(base_url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Erro na requisição ao Scopus: {response.status_code} - {response.text}")

    return response.json()
