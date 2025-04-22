# app/pico_analyzer.py

import spacy
from langdetect import detect
from deep_translator import GoogleTranslator
import json
import os

# Load the scispaCy model for biomedical English texts
nlp = spacy.load("en_core_sci_sm")

# File to save the user's PICOT pattern memory (for light adaptive learning)
USER_PATTERN_MEMORY = os.path.join(os.path.dirname(__file__), "picot_learning_memory.json")

# Initialize or load adaptive memory
if os.path.exists(USER_PATTERN_MEMORY):
    with open(USER_PATTERN_MEMORY, "r", encoding="utf-8") as f:
        user_memory = json.load(f)
else:
    user_memory = {}

def save_memory():
    with open(USER_PATTERN_MEMORY, "w", encoding="utf-8") as f:
        json.dump(user_memory, f, indent=2)

def analyze_question(question):
    # 1) Detect language
    detected_lang = detect(question)
    question_en = question

    # 2) If não for inglês, tente traduzir
    if detected_lang != "en":
        try:
            question_en = GoogleTranslator(source='auto', target='en').translate(question)
        except Exception as e:
            # Se falhar por limite de requisições, tenta o batch
            try:
                question_en = GoogleTranslator(source='auto', target='en') \
                                .translate_batch([question])[0]
            except Exception:
                # Último recurso: mantém o original
                question_en = question
    # força lowercase para o NLP
    doc = nlp(question_en.lower())
    tokens = [token.text for token in doc]

    mesh_mapping = {
        "population": {
            "patients": "Patients",
            "children": "Child",
            "adults": "Adult",
            "elderly": "Aged",
            "individuals": "Humans"
        },
        "intervention": {
            "exercise": "Exercise Therapy",
            "treatment": "Therapeutics",
            "therapy": "Therapy",
            "intervention": "Intervention",
            "drug": "Pharmaceutical Preparations"
        },
        "comparison": {
            "placebo": "Placebos",
            "control": "Control",
            "standard": "Standard of Care",
            "no treatment": "No Treatment"
        },
        "outcome": {
            "pain": "Pain",
            "function": "Functional Outcome",
            "mobility": "Mobility",
            "recovery": "Recovery",
            "strength": "Muscle Strength"
        },
        "time": {
            "weeks": "Weeks",
            "months": "Months",
            "days": "Days",
            "years": "Years"
        }
    }

    def find_term(term_type, fallback_terms, mapping):
        # 1) Adaptive memory
        for token in tokens:
            if token in user_memory.get(term_type, []):
                return mapping.get(term_type, {}).get(token.lower(), token)

        # 2) Keywords de fallback
        for token in tokens:
            for kw in fallback_terms:
                if kw in token:
                    user_memory.setdefault(term_type, []).append(token)
                    save_memory()
                    return mapping.get(term_type, {}).get(kw, kw)
        return ""

    pico_result = {
        "language": detected_lang,
        "question_en": question_en,
        "population":    find_term("population",   ["patients","children","adults","elderly","individuals"], mesh_mapping),
        "intervention":  find_term("intervention", ["exercise","treatment","therapy","intervention","drug"],     mesh_mapping),
        "comparison":    find_term("comparison",   ["placebo","control","standard","no treatment"],          mesh_mapping),
        "outcome":       find_term("outcome",      ["pain","function","mobility","recovery","strength"],    mesh_mapping),
        "time":          find_term("time",         ["weeks","months","days","years"],                      mesh_mapping)
    }

    return pico_result
