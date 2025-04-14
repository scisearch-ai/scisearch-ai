# app/triage_decorator.py

import re

def highlight_terms(abstract: str, pico: dict) -> str:
    """
    Recebe um resumo (abstract) e uma estrutura PICOT (como dicionário) e
    retorna o resumo com os termos PICOT destacados utilizando a tag <mark>.
    
    Exemplo:
        Input: abstract = "This study on elderly patients..."
               pico = {"population": "elderly", "intervention": "exercise", ...}
        Output: texto com "elderly" e "exercise" destacados
    """
    highlighted = abstract
    # Lista dos campos PICOT a serem buscados
    fields = ["population", "intervention", "comparison", "outcome", "time"]
    for field in fields:
        term = pico.get(field, "")
        if term:
            # Cria um padrão de busca ignorando case, com limites de palavra
            pattern = re.compile(r'\b' + re.escape(term) + r'\b', re.IGNORECASE)
            highlighted = pattern.sub(lambda m: f"<mark>{m.group(0)}</mark>", highlighted)
    return highlighted

def triage_article(abstract: str, pico: dict) -> dict:
    """
    Processa o resumo (abstract) aplicando uma triagem simples com base na
    presença dos termos da estrutura PICOT.
    Utiliza a função highlight_terms para realçar os termos no resumo e
    retorna uma decisão simples (inclusão ou exclusão) acompanhada de uma breve
    justificativa.
    
    Critério de exemplo:
        - Se pelo menos 2 dos componentes PICOT forem encontrados, a decisão é "included";
        - Caso contrário, "excluded".
    """
    # Obtém o resumo com os termos destacados
    highlighted_abstract = highlight_terms(abstract, pico)
    
    # Conta quantos termos PICOT aparecem no resumo (buscando cada termo no texto)
    count = 0
    for field in ["population", "intervention", "comparison", "outcome", "time"]:
        term = pico.get(field, "")
        if term and re.search(r'\b' + re.escape(term) + r'\b', abstract, re.IGNORECASE):
            count += 1
            
    decision = "included" if count >= 2 else "excluded"
    explanation = f"Detected {count} PICOT components in the abstract."
    
    return {
        "abstract": abstract,
        "highlighted": highlighted_abstract,
        "decision": decision,
        "explanation": explanation
    }
