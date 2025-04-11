import spacy
from langdetect import detect
from deep_translator import GoogleTranslator

# Load SciSpaCy model
nlp = spacy.load("en_core_sci_sm")

def analyze_question(question):
    # Detect language
    detected_lang = detect(question)
    if detected_lang != "en":
        question_en = GoogleTranslator(source='auto', target='en').translate(question)
    else:
        question_en = question

    doc = nlp(question_en.lower())

    # Heuristics for detecting PICOT components
    tokens = [token.text for token in doc]

    population_terms = ["patients", "children", "adults", "elderly", "individuals", "subjects"]
    intervention_terms = ["treatment", "therapy", "exercise", "intervention", "drug", "medication"]
    comparison_terms = ["placebo", "control", "standard", "no treatment"]
    outcome_terms = ["pain", "function", "mobility", "recovery", "strength", "fatigue"]
    time_terms = ["weeks", "months", "years", "days", "sessions"]

    def find_term(term_list):
        for token in tokens:
            for keyword in term_list:
                if keyword in token:
                    return keyword
        return "unspecified"

    pico_result = {
        "language": detected_lang,
        "question_en": question_en,
        "population": find_term(population_terms),
        "intervention": find_term(intervention_terms),
        "comparison": find_term(comparison_terms),
        "outcome": find_term(outcome_terms),
        "time": find_term(time_terms)
    }

    return pico_result
