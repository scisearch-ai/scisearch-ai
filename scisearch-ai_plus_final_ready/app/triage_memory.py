# app/triage_memory.py

import json
from collections import defaultdict
from typing import Dict, List

# Memória central (para uso em todos os usuários)
LEARNING_MEMORY: Dict[str, List[Dict]] = defaultdict(list)

def record_decision(summary: str, decision: str, explanation: str, pico: dict):
    """
    Armazena a decisão de inclusão/exclusão junto com explicação e estrutura PICOT.
    """
    key = summary.strip().lower()
    LEARNING_MEMORY[key].append({
        "decision": decision,
        "explanation": explanation,
        "pico": pico
    })

def learn_from_history(summary: str, pico: dict) -> str:
    """
    Tenta encontrar decisões anteriores semelhantes e retorna uma sugestão.
    """
    key = summary.strip().lower()
    history = LEARNING_MEMORY.get(key, [])

    if not history:
        return "undecided"

    # Sistema simples de maioria
    decisions = [entry["decision"] for entry in history]
    included = decisions.count("included")
    excluded = decisions.count("excluded")
    return "included" if included >= excluded else "excluded"

def load_memory(filepath="learning_memory.json"):
    """
    Reimporta o histórico de aprendizagem para uso posterior.
    """
    global LEARNING_MEMORY
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            LEARNING_MEMORY = defaultdict(list, data)
    except FileNotFoundError:
        pass

def save_memory(filepath="learning_memory.json"):
    """
    Exporta o histórico para um arquivo JSON (opcional).
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(LEARNING_MEMORY, f, indent=2, ensure_ascii=False)
