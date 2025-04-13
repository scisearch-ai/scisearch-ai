# app/triage_interface.py

from flask import Blueprint, request, jsonify
from app.triage_engine import triage_abstract
from app.triage_memory import update_memory

triage_bp = Blueprint("triage", __name__)

@triage_bp.route("/triage", methods=["POST"])
def triage():
    """
    Endpoint da Fase 7:
    Recebe o resumo do artigo e a estrutura PICOT.
    Realiza triagem automática e sugere decisão com justificativa curta.
    """
    try:
        data = request.get_json()

        abstract = data.get("abstract", "")
        pico = data.get("pico", {})
        user_decision = data.get("user_decision", None)  # inclusão/exclusão manual

        if not abstract or not pico:
            return jsonify({"error": "Resumo ou estrutura PICOT ausente."}), 400

        # Realiza triagem automatizada
        decision_result = triage_abstract(abstract, pico)

        # Se o usuário confirmou ou alterou a sugestão da IA:
        if user_decision in ["include", "exclude"]:
            update_memory(abstract, pico, user_decision)

        return jsonify(decision_result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
