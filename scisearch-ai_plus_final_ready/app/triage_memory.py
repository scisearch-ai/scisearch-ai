# app/triage_memory.py

import json
from collections import defaultdict
from typing import Dict, List, Any

# Memória central para uso em todos os usuários
LEARNING_MEMORY: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

def record_decision(summary: str, decision: str, explanation: str, pico: dict) -> None:
    """
    Armazena a decisão de inclusão/exclusão juntamente com a explicação e a estrutura PICOT.
    """
    key = summary.strip().lower()
    LEARNING_MEMORY[key].append({
        "decision": decision,
        "explanation": explanation,
        "pico": pico
    })

def learn_from_history(summary: str, pico: dict) -> str:
    """
    Tenta encontrar decisões anteriores semelhantes com base no resumo e retorna uma sugestão:
    'included', 'excluded' ou 'undecided' se não houver histórico.
    
    Nota: O parâmetro pico não está sendo usado atualmente, mas pode ser incorporado em análises futuras.
    """
    key = summary.strip().lower()
    history = LEARNING_MEMORY.get(key, [])

    if not history:
        return "undecided"

    # Sistema simples baseado na maioria das decisões
    decisions = [entry["decision"] for entry in history]
    included = decisions.count("included")
    excluded = decisions.count("excluded")

    return "included" if included >= excluded else "excluded"

def export_learning_memory(filepath: str = "learning_memory.json") -> None:
    """
    Exporta o histórico de decisões para um arquivo JSON.
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(LEARNING_MEMORY, f, indent=2, ensure_ascii=False)

def import_learning_memory(filepath: str = "learning_memory.json") -> None:
    """
    Reimporta o histórico de aprendizagem a partir de um arquivo JSON para uso posterior.
    Se o arquivo não existir, mantém o histórico vazio.
    """
    global LEARNING_MEMORY
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Recria o defaultdict mantendo os dados importados
            LEARNING_MEMORY = defaultdict(list, data)
    except FileNotFoundError:
        pass
