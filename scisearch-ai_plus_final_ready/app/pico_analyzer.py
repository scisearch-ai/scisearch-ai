import spacy
from langdetect import detect
from deep_translator import GoogleTranslator

# Modelos por idioma
spacy_models = {
    "en": spacy.load("en_core_sci_sm"),
    "pt": spacy.load("pt_core_news_sm"),
    "es": spacy.load("es_core_news_sm"),
    "fr": spacy.load("fr_core_news_sm")
}

def analyze_question(question):
    # Detecta idioma da pergunta
    detected_lang = detect(question)
    nlp = spacy_models.get(detected_lang, spacy_models["en"])

    # Traduz se não for inglês
    if detected_lang != "en":
        question_en = GoogleTranslator(source=detected_lang, target="en").translate(question)
    else:
        question_en = question

    doc = spacy_models["en"](question_en.lower())

    # Heurística simples baseada em palavras-chave
    tokens = [token.text for token in doc]

    def extract_term(keywords):
        for i, token in enumerate(tokens):
            if token in keywords:
                return " ".join(tokens[i:i+4])
        return "unspecified"

    population_terms = ["patients", "children", "adults", "elderly", "diabetics"]
    intervention_terms = ["exercise", "treatment", "therapy", "training", "drug"]
    comparison_terms = ["placebo", "no treatment", "control", "none"]
    outcome_terms = ["pain", "function_
