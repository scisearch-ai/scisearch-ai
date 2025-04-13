# triage_decorator.py
import re
from collections import defaultdict
from app.triage_memory import TriageMemory

# 🧠 Inicialização da memória de aprendizado global
memory = TriageMemory()

def triage_article(pico, abstract):
    """
    Analisa automaticamente o abstract para decidir inclusão/exclusão com base na estrutura PICOT.
    Retorna um dicionário com decisão e justificativa.
    """
    decision = "exclude"
    justification = "This study does not clearly match the PICOT structure provided."

    # 🔍 Identificação simples por palavras-chave (substituível por NLP posterior)
    found = defaultdict(bool)
    tokens = {
        "P": pico.get("population", "").lower(),
        "I": pico.get("intervention", "").lower(),
        "O": pico.get("outcome", "").lower(),
    }

    abstract_lower = abstract.lower()
    
    for key, term in tokens.items():
        if term and term in abstract_lower:
            found[key] = True

    # ✅ Critério básico para inclusão: P, I e O presentes
    if all(found.values()):
        decision = "include"
        justification = "Population, intervention and outcome are clearly mentioned in the abstract."

    # 📚 Verifica se já existe decisão aprendida
    learned = memory.check_learned(pico, abstract)
    if learned:
        return learned

    # 📥 Salva a decisão para aprendizado futuro
    memory.learn(pico, abstract, decision, justification)

    return {
        "decision": decision,
        "justification": justification
    }
