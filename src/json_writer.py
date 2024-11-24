import json

def write_json_to_file(json_structure, output_path):
    wrapped_structure = {
        "tags": json_structure,
        "type": "UdtType"
    }
    with open(output_path, "w") as json_file:
        json.dump(wrapped_structure, json_file, indent=4)
