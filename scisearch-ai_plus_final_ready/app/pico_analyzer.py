# FASE 1 – Enhanced automatic PICOT structure recognition with editable field and adaptive intelligence

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
    with open(USER_PATTERN_MEMORY, "r") as f:
        user_memory = json.load(f)
else:
    user_memory = {}

def save_memory():
    with open(USER_PATTERN_MEMORY, "w") as f:
        json.dump(user_memory, f, indent=2)

def analyze_question(question):
    # Detect the language of the question
    detected_lang = detect(question)
    if detected_lang != "en":
        # Translate to English
        question_en = GoogleTranslator(source='auto', target='en').translate(question)
    else:
        question_en = question

    # Process the question text with spaCy
    doc = nlp(question_en.lower())
    tokens = [token.text for token in doc]

    # Mapping dictionaries for converting fallback keywords to MeSH terms
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

    # Function to find a term in the tokens using both adaptive memory and fallback terms.
    def find_term(term_type, fallback_terms, mapping):
        # Check if any term from user's memory is in the tokens
        memory_terms = user_memory.get(term_type, [])
        for token in tokens:
            if token in memory_terms:
                # If found, map to MeSH if possible and return
                for key in mapping.get(term_type, {}):
                    if key in token.lower():
                        return mapping[term_type][key]
                return token

        # Fallback: search for fallback keywords in tokens
        for token in tokens:
            for keyword in fallback_terms:
                if keyword in token:
                    # Save this token in the adaptive memory if not already present
                    if token not in user_memory.get(term_type, []):
                        user_memory.setdefault(term_type, []).append(token)
                        save_memory()
                    # Map to MeSH term if available in the mapping dictionary
                    if term_type in mapping:
                        for key in mapping[term_type]:
                            if key in token.lower():
                                return mapping[term_type][key]
                    return keyword
        return ""

    pico_result = {
        "language": detected_lang,
        "question_en": question_en,
        "population": find_term("population", ["patients", "children", "adults", "elderly", "individuals"], mesh_mapping),
        "intervention": find_term("intervention", ["exercise", "treatment", "therapy", "intervention", "drug"], mesh_mapping),
        "comparison": find_term("comparison", ["placebo", "control", "standard", "no treatment"], mesh_mapping),
        "outcome": find_term("outcome", ["pain", "function", "mobility", "recovery", "strength"], mesh_mapping),
        "time": find_term("time", ["weeks", "months", "days", "years"], mesh_mapping)
    }

    return pico_result
