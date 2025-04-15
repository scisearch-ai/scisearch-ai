import json
import os

# Define the path for the file that will store the user's corrections/memory.
USER_CORRECTIONS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user_corrections.json")

def load_memory():
    """
    Loads the user memory data from the JSON file.

    Returns:
        dict: The stored memory data. Returns an empty dict if the file does not exist.
    """
    if os.path.exists(USER_CORRECTIONS_FILE):
        with open(USER_CORRECTIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_memory(memory):
    """
    Saves the user memory data to the JSON file.

    Args:
        memory (dict): The dictionary containing the memory data.
    """
    with open(USER_CORRECTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)

def save_user_corrections(corrected_picot):
    """
    Saves the corrected PICOT structure provided by the user into the memory.
    
    Args:
        corrected_picot (dict): The corrected PICOT structure.
    """
    memory = load_memory()
    # Use a key 'corrections' to store a list of user corrections.
    if "corrections" not in memory:
        memory["corrections"] = []
    memory["corrections"].append(corrected_picot)
    save_memory(memory)

def update_memory(new_data):
    """
    Updates the memory with new data by merging it with the existing memory.
    
    Args:
        new_data (dict): A dictionary with new memory data to be merged.
    """
    memory = load_memory()
    memory.update(new_data)
    save_memory(memory)
