import json
import os

def load_json(filepath, default=None):
    """Load a JSON file and return its data or a default value if not found or invalid."""
    if not os.path.exists(filepath):
        return default if default is not None else {}

    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        # Handle empty or corrupt JSON
        return default if default is not None else {}

def save_json(filepath, data):
    """Save data to a JSON file with indentation."""
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)

def load_json_data(filepath):
    """Load data from a JSON file. Returns empty list if file does not exist."""
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            return json.load(file)
    else:
        return []
