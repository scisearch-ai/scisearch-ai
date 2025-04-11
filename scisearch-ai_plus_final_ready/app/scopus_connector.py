import requests
import os

API_KEY = os.getenv("SCOPUS_API_KEY")

def fetch_scopus_data(query, study_types=[], year_range=None):
    headers = {
        "X-ELS-APIKey": API_KEY,
        "Accept": "application/json"
    }

    base_url = "https://api.elsevier.com/content/search/scopus"
    params = {
        "query": query,
        "count": 50,
        "sort": "relevancy"
    }

    if year_range:
        params["date"] = f"{year_range[0]}-{year_range[1]}"

    response = requests.get(base_url, headers=headers, params=params)
    if response.status_code != 200:
        return []

    data = response.json()
    entries = data.get("search-results", {}).get("entry", [])

    articles = []
    for entry in entries:
        title = entry.get("dc:title", "")
        source = entry.get("prism:publicationName", "")
        authors = entry.get("dc:creator", "")
        pubdate = entry.get("prism:coverDate", "")
        link = entry.get("prism:url", "")

        articles.append({
            "title": title,
            "source": source,
            "authors": authors,
            "pubdate": pubdate,
            "link": link,
            "database": "Scopus"
        })

    return articles
