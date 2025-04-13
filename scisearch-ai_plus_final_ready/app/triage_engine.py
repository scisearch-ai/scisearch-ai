# triage_engine.py
from app.triage_memory import TriageMemory
from app.triage_decorator import highlight_terms

class TriageEngine:
    def __init__(self):
        self.memory = TriageMemory()

    def evaluate_article(self, article, pico_structure):
        """
        Analisa automaticamente um artigo com base no resumo e na estrutura PICOT.
        """
        abstract = article.get("abstract", "").lower()
        title = article.get("title", "")
        source = article.get("source", "Unknown")
        decision = self.memory.predict(abstract, pico_structure)

        # Justificativa automática
        justification = self._generate_justification(abstract, pico_structure, decision)

        return {
            "title": title,
            "abstract": highlight_terms(abstract, pico_structure),
            "decision": decision,
            "justification": justification,
            "source": source,
            "editable": True  # usuário pode alterar
        }

    def update_decision(self, abstract, pico_structure, decision):
        """
        Atualiza a memória com a decisão confirmada ou corrigida pelo usuário.
        """
        self.memory.learn(abstract, pico_structure, decision)

    def _generate_justification(self, abstract, pico, decision):
        terms_used = []
        for key in ["population", "intervention", "outcome"]:
            value = pico.get(key, "").lower()
            if value and value in abstract:
                terms_used.append(key)

        if decision == "included":
            return f"Included because it contains relevant {', '.join(terms_used)}."
        else:
            return f"Excluded due to missing alignment with PICOT focus."
