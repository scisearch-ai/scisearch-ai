# FASE 1 – Atualização de reconhecimento automático da estrutura PICOT com campo editável e inteligência adaptativa

# Arquivo: pico_analyzer.py

import spacy
from langdetect import detect
from deep_translator import GoogleTranslator
import json
import os

nlp = spacy.load("en_core_sci_sm")

# Caminho para salvar preferências do usuário (auto aprendizado leve)
USER_PATTERN_MEMORY = "app/picot_learning_memory.json"

# Inicializa ou carrega memória adaptativa
if os.path.exists(USER_PATTERN_MEMORY):
    with open(USER_PATTERN_MEMORY, "r") as f:
        user_memory = json.load(f)
else:
    user_memory = {}

def save_memory():
    with open(USER_PATTERN_MEMORY, "w") as f:
        json.dump(user_memory, f, indent=2)

def analyze_question(question):
    detected_lang = detect(question)
    if detected_lang != "en":
        question_en = GoogleTranslator(source='auto', target='en').translate(question)
    else:
        question_en = question

    doc = nlp(question_en.lower())
    tokens = [token.text for token in doc]

    # Heurísticas baseadas em contexto aprendido do usuário (auto aprendizado leve)
    def find_term(term_type, fallback_terms):
        # Tenta encontrar termo com base na memória de padrões do usuário
        memory_terms = user_memory.get(term_type, [])
        for token in tokens:
            if token in memory_terms:
                return token

        # Fallback para termos padrão
        for token in tokens:
            for keyword in fallback_terms:
                if keyword in token:
                    # Aprendizado simples: salva esse termo na memória do usuário
                    if token not in user_memory.get(term_type, []):
                        user_memory.setdefault(term_type, []).append(token)
                        save_memory()
                    return keyword
        return ""

    pico_result = {
        "language": detected_lang,
        "question_en": question_en,
        "population": find_term("population", ["patients", "children", "adults", "elderly", "individuals"]),
        "intervention": find_term("intervention", ["exercise", "treatment", "therapy", "intervention", "drug"]),
        "comparison": find_term("comparison", ["placebo", "control", "standard", "no treatment"]),
        "outcome": find_term("outcome", ["pain", "function", "mobility", "recovery", "strength"]),
        "time": find_term("time", ["weeks", "months", "days", "years"]),
    }

    return pico_result
