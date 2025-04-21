# FASE 1 – Enhanced automatic PICOT structure recognition
# File: pico_analyzer.py

import spacy
from langdetect import detect
from deep_translator import GoogleTranslator
import json
import os

# Load the scispaCy model for biomedical English texts
nlp = spacy.load("en_core_sci_sm")

# File to save the user's PICOT pattern memory (for light adaptive learning)
USER_PATTERN_MEMORY = "app/picot_learning_memory.json"

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
    # Detect language and translate if needed
    detected_lang = detect(question)
    if detected_lang != "en":
        question_en = GoogleTranslator(source='auto', target='en').translate(question)
    else:
        question_en = question

    # Tokenize via spaCy
    doc = nlp(question_en.lower())
    tokens = [token.text for token in doc]

    # MeSH mapping dictionaries
    mesh_mapping = {
        "population": {
            "patients":       "Patients",
            "children":       "Child",
            "adults":         "Adult",
            "elderly":        "Aged",
            "individuals":    "Humans"
        },
        "intervention": {
            "exercise":               "Exercise Therapy",
            "treatment":              "Therapeutics",
            "therapy":                "Therapy",
            "intervention":           "Intervention",
            "drug":                   "Pharmaceutical Preparations"
        },
        "comparison": {
            "placebo":        "Placebos",
            "control":        "Control",
            "standard":       "Standard of Care",
            "no treatment":   "No Treatment"
        },
        "outcome": {
            "pain":        "Pain",
            "function":    "Functional Outcome",
            "mobility":    "Mobility",
            "recovery":    "Recovery",
            "strength":    "Muscle Strength"
        },
        "time": {
            "weeks":   "Weeks",
            "months":  "Months",
            "days":    "Days",
            "years":   "Years"
        }
    }

    # Priority lists
    fallback_lists = {
        "population":   ["patients", "children", "adults", "elderly", "individuals"],
        "intervention": ["exercise", "treatment", "therapy", "intervention", "drug"],
        "comparison":   ["placebo", "control", "standard", "no treatment"],
        "outcome":      ["pain", "function", "mobility", "recovery", "strength"],
        "time":         ["weeks", "months", "days", "years"],
    }

    def find_term(term_type):
        """
        1) Se 'patients' aparecer em qualquer token, retorna imediatamente 'Patients'.
        2) Verifica memória adaptativa.
        3) Percorre fallback keywords na ordem de prioridade, buscando em todos os tokens.
        """
        mapping = mesh_mapping.get(term_type, {})
        fallbacks = fallback_lists.get(term_type, [])

        # 1) Prioridade absoluta para 'patients' no tipo population
        if term_type == "population" and any(tok == "patients" for tok in tokens):
            return mapping["patients"]

        # 2) Memória adaptativa
        for mem in user_memory.get(term_type, []):
            if any(mem in tok for tok in tokens):
                # tenta mapear via MeSH
                for key, mesh in mapping.items():
                    if key in mem:
                        return mesh
                return mem

        # 3) Fallback por prioridade de lista
        for keyword in fallbacks:
            for tok in tokens:
                if keyword in tok:
                    # registra na memória
                    if tok not in user_memory.get(term_type, []):
                        user_memory.setdefault(term_type, []).append(tok)
                        save_memory()
                    # retorna mapeamento MeSH se existir
                    return mapping.get(keyword, keyword)

        # se nada encontrado
        return ""

    pico_result = {
        "language": detected_lang,
        "question_en": question_en,
        "population":   find_term("population"),
        "intervention": find_term("intervention"),
        "comparison":   find_term("comparison"),
        "outcome":      find_term("outcome"),
        "time":         find_term("time")
    }

    return pico_result
