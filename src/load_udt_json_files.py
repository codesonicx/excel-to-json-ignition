import json
from pathlib import Path

def load_base_udt_data(file_paths):
    """
    Loads the base UDT JSON files from a list of paths.

    Args:
    - file_paths (list): A list of file paths as strings or Path objects.

    Returns:
    - dict: A dictionary containing the base UDT data, with keys derived from file names.
    """
    base_udt_data = {}
    for file_path in file_paths:
        file_name = Path(file_path).stem  # Get the file name without extension
        with open(file_path, 'r') as f:
            base_udt_data[file_name] = json.load(f)
    return base_udt_data