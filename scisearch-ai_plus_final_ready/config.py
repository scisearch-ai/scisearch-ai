# config.py

import os
from dotenv import load_dotenv

# Carrega as variáveis do .env, se existir
load_dotenv()

class Config:
    # Variáveis de ambiente
    PUBMED_API_KEY = os.getenv("PUBMED_API_KEY")
    SCOPUS_API_KEY = os.getenv("SCOPUS_API_KEY")
    DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en")
    RESULTS_LIMIT = int(os.getenv("RESULTS_LIMIT", 50))
    TIME_RANGE = os.getenv("TIME_RANGE", "all")
    ENABLE_TRANSLATION = os.getenv("ENABLE_TRANSLATION", "true").lower() == "true"

    # Logging básico
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    TESTING = os.getenv("TESTING", "false").lower() == "true"
