import requests
from bs4 import BeautifulSoup
import os

API_KEY = os.getenv("PUBMED_API_KEY")

def fetch_pubmed_data(query, study_types=[], year_range=None):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 50,
        "api_key": API_KEY
    }

    if year_range:
        params["mindate"] = year_range[0]
        params["maxdate"] = year_range[1]
        params["datetype"] = "pdat"

    response = requests.get(base_url, params=params)
    id_list = response.json().get("esearchresult", {}).get("idlist", [])

    if not id_list:
        return []

    summaries_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    summaries_params = {
        "db": "pubmed",
        "id": ",".join(id_list),
        "retmode": "json",
        "api_key": API_KEY
    }

    summaries_response = requests.get(summaries_url, params=summaries_params)
    summaries = summaries_response.json().get("result", {})

    articles = []
    for uid in id_list:
        item = summaries.get(uid, {})
        title = item.get("title", "")
        source = item.get("source", "")
        authors = ", ".join([au["name"] for au in item.get("authors", []) if "name" in au])
        pubdate = item.get("pubdate", "")
        link = f"https://pubmed.ncbi.nlm.nih.gov/{uid}/"

        articles.append({
            "title": title,
            "source": source,
            "authors": authors,
            "pubdate": pubdate,
            "link": link,
            "database": "PubMed"
        })

    return articles
