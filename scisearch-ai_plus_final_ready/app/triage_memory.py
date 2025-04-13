# app/triage_memory.py

import json
from collections import defaultdict

# Memória compartilhada entre usuários (poderia ser um banco no futuro)
class TriageMemory:
    def __init__(self):
        self.memory = defaultdict(list)  # {'included': [...], 'excluded': [...]} 

    def record_decision(self, decision_type, summary_text, pico):
        # Armazena o resumo e a estrutura PICOT que justificaram a decisão
        self.memory[decision_type].append({
            "summary": summary_text,
            "pico": pico
        })

    def learn_keywords(self):
        # Aprende com decisões anteriores baseando-se na frequência de termos por tipo de decisão
        keywords = {"included": defaultdict(int), "excluded": defaultdict(int)}

        for decision_type in ["included", "excluded"]:
            for record in self.memory[decision_type]:
                for key in ["Population", "Intervention", "Outcome"]:
                    term = record["pico"].get(key, "").lower()
                    if term:
                        keywords[decision_type][term] += 1

        return keywords

    def predict_decision(self, summary_text, pico):
        # Estratégia simples de inferência baseada na similaridade de palavras-chave
        keywords = self.learn_keywords()
        score = {"included": 0, "excluded": 0}

        for decision_type in ["included", "excluded"]:
            for key in ["Population", "Intervention", "Outcome"]:
                term = pico.get(key, "").lower()
                if term in summary_text.lower():
                    score[decision_type] += keywords[decision_type].get(term, 0)

        if score["included"] >= score["excluded"]:
            return "included"
        else:
            return "excluded"

# Instância global para uso no app
triage_memory = TriageMemory()
