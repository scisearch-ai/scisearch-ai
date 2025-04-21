# app/triage_interface.py

from flask import Blueprint, request, jsonify
from app.triage_engine import triage_abstract
from app.triage_memory import save_user_corrections

triage_bp = Blueprint("triage", __name__)

@triage_bp.route("/triage", methods=["POST"])
def triage():
    """
    Endpoint da Fase 7:
    Recebe o resumo do artigo e a estrutura PICOT.
    Realiza triagem automática e sugere decisão com justificativa curta.
    """
    try:
        data = request.get_json() or {}
        abstract      = data.get("abstract", "").strip()
        pico          = data.get("pico", {})
        user_decision = data.get("user_decision")  # "include" ou "exclude"

        if not abstract or not pico:
            return jsonify({"error": "Resumo ou estrutura PICOT ausente."}), 400

        # Triage automático
        decision_result = triage_abstract(abstract, pico)

        # Se o usuário fez uma decisão manual, salvamos para aprendizado
        if user_decision in ["include", "exclude"]:
            save_user_corrections({
                "abstract": abstract,
                "pico": pico,
                "decision": user_decision
            })

        return jsonify(decision_result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
