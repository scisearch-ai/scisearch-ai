# app/triage_memory.py

import json
from collections import defaultdict
from typing import Dict, List

# Memória central (para uso em todos os usuários)
LEARNING_MEMORY: Dict[str, List[Dict]] = defaultdict(list)

def record_decision(summary: str, decision: str, explanation: str, pico: dict):
    """
    Armazena a decisão de inclusão/exclusão junto com a explicação e a estrutura PICOT.
    
    Args:
        summary (str): Resumo do artigo.
        decision (str): Decisão, por exemplo, "included" ou "excluded".
        explanation (str): Breve justificativa da decisão.
        pico (dict): Estrutura PICOT associada.
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
    Se não houver histórico, retorna "undecided".
    
    Args:
        summary (str): Resumo do artigo.
        pico (dict): Estrutura PICOT associada (não utilizada na lógica atual, mas incluída para futuros refinamentos).
    
    Returns:
        str: "included", "excluded" ou "undecided"
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

def export_learning_memory(filepath="learning_memory.json"):
    """
    Exporta o histórico de aprendizagem para um arquivo JSON.
    
    Args:
        filepath (str): Caminho para o arquivo de saída.
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(LEARNING_MEMORY, f, indent=2, ensure_ascii=False)

def import_learning_memory(filepath="learning_memory.json"):
    """
    Reimporta o histórico de aprendizagem a partir de um arquivo JSON para uso posterior.
    
    Args:
        filepath (str): Caminho para o arquivo de entrada.
    """
    global LEARNING_MEMORY
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            LEARNING_MEMORY = defaultdict(list, data)
    except FileNotFoundError:
        pass

# Classe que encapsula as funcionalidades de memória para ser importada por outros módulos
class TriageMemory:
    @staticmethod
    def record(summary: str, decision: str, explanation: str, pico: dict):
        """
        Registra uma decisão de triagem.
        """
        record_decision(summary, decision, explanation, pico)

    @staticmethod
    def suggest(summary: str, pico: dict) -> str:
        """
        Retorna uma sugestão baseada no histórico de decisões para o resumo dado.
        """
        return learn_from_history(summary, pico)

    @staticmethod
    def export(filepath="learning_memory.json"):
        """
        Exporta o histórico para um arquivo JSON.
        """
        export_learning_memory(filepath)

    @staticmethod
    def import_memory(filepath="learning_memory.json"):
        """
        Importa o histórico do arquivo JSON para a memória.
        """
        import_learning_memory(filepath)

# Aliases para compatibilidade com outros módulos
load_memory = import_learning_memory
save_memory = export_learning_memory
update_memory = record_decision  # Adiciona o alias update_memory para atualizar a memória
