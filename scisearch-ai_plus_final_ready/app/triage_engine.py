# app/triage_engine.py

from app.triage_decorator import triage_article

def triage_abstract(abstract: str, pico: dict) -> dict:
    """
    Processa o abstract com base na estrutura PICOT fornecida.
    Utiliza a função triage_article (definida em triage_decorator) para
    realizar a avaliação e retornar a decisão (incluído/excluído) juntamente
    com a justificativa e o abstract com os termos destacados.
    
    Args:
        abstract (str): O resumo do artigo.
        pico (dict): A estrutura PICOT para orientar a triagem.

    Returns:
        dict: Resultado da triagem contendo o abstract original,
              o abstract com termos destacados, a decisão e a justificativa.
    """
    return triage_article(abstract, pico)
