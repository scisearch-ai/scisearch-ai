import requests
import os


def search_pubmed(query: str, api_key: str = None, max_results: int = 20) -> dict:
    """
    Realiza uma busca na base PubMed usando a API do NCBI E-Utilities.
    
    Parâmetros:
        - query (str): termo de busca em formato livre ou estruturado (ex: 'diabetes AND exercise').
        - api_key (str, opcional): chave de API do NCBI para melhorar o limite de requisições.
        - max_results (int): número máximo de resultados a serem retornados.

    Retorno:
        - dict: resposta da API em formato JSON contendo os IDs dos artigos encontrados.
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results
    }

    # Usa a chave do ambiente se não for passada diretamente
    if not api_key:
        api_key = os.environ.get("PUBMED_API_KEY")
    if api_key:
        params["api_key"] = api_key

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erro na requisição ao PubMed: {response.status_code} - {response.text}")

# Comentário opcional para referência futura:
# Add search_pubmed function to pubmed_connector
