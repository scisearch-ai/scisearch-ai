# app/triage_memory.py
import json
import os

# Caminho para o arquivo que guardará as correções dos usuários
USER_CORRECTIONS_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "user_corrections.json"
)

def load_memory() -> dict:
    """
    Carrega a memória de correções dos usuários.
    Retorna um dict vazio se o arquivo não existir.
    """
    if os.path.exists(USER_CORRECTIONS_FILE):
        with open(USER_CORRECTIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_memory(memory: dict) -> None:
    """
    Salva o dict de memória no disco.
    """
    with open(USER_CORRECTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)

def save_user_corrections(corrected_picot: dict) -> None:
    """
    Adiciona uma correção de PICOT feita pelo usuário.
    """
    memory = load_memory()
    memory.setdefault("corrections", []).append(corrected_picot)
    save_memory(memory)

def update_memory(new_data: dict) -> None:
    """
    Mescla novos dados de memória aos já existentes.
    """
    memory = load_memory()
    memory.update(new_data)
    save_memory(memory)
