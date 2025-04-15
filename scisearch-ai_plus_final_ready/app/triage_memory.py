import json
import os

# Define o caminho para o arquivo que armazenará as correções do usuário
USER_CORRECTIONS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user_corrections.json")

def load_memory():
    """
    Loads the user corrections memory from the JSON file.
    
    Returns:
        dict: A dictionary with saved corrections. Returns an empty dict if the file does not exist.
    """
    if os.path.exists(USER_CORRECTIONS_FILE):
        with open(USER_CORRECTIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_memory(memory):
    """
    Saves the user corrections memory to the JSON file.
    
    Args:
        memory (dict): The dictionary containing the corrections data.
    """
    with open(USER_CORRECTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)

def save_user_corrections(corrected_picot):
    """
    Saves the corrected PICOT structure provided by the user into the memory.
    This function appends the corrected structure to a list of corrections.
    
    Args:
        corrected_picot (dict): The corrected PICOT structure.
    """
    memory = load_memory()
    # Usaremos uma chave "corrections" para armazenar as correções em uma lista
    if "corrections" not in memory:
        memory["corrections"] = []
    memory["corrections"].append(corrected_picot)
    save_memory(memory)
