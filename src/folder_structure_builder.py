import re
import copy
from typing import List, Dict, Any

def convert_brackets_to_parentheses(name: str) -> str:
    """Converts brackets to parentheses in a string, e.g., 'array[0]' to 'array(0)'."""
    return re.sub(r"\[(\d+)\]", r"(\1)", name)

def overwrite_udt_tags(udt_tags: List[Dict[str, Any]], bit_descriptions: Dict[str, str]) -> List[Dict[str, Any]]:
    """
    Overwrites the 'value' of tags within 'bitsDescription' based on provided bit descriptions.

    Parameters:
    - udt_tags: The list of tags from the UDT JSON.
    - bit_descriptions: A dictionary mapping bit numbers (as strings) to descriptions.

    Returns:
    - The modified list of UDT tags.
    """
    for tag in udt_tags:
        if tag["name"] == "bitsDescription" and tag["tagType"] == "Folder":
            for bit_tag in tag["tags"]:
                match = re.match(r"^(\d+)_description$", bit_tag["name"])
                if match:
                    bit_number = match.group(1)
                    if bit_number in bit_descriptions:
                        bit_tag["value"] = bit_descriptions[bit_number]
    return udt_tags

def build_folder_hierarchy(prefix: str, folder_structure: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Builds the folder hierarchy based on the given prefix.

    Parameters:
    - prefix: The prefix representing the folder hierarchy.
    - folder_structure: The shared folder structure to modify.

    Returns:
    - The current level in the folder structure after building the hierarchy.
    """
    path_components = prefix.split('.')
    current_level = folder_structure

    for component in path_components:
        component_name = convert_brackets_to_parentheses(component)
        existing_folder = next(
            (item for item in current_level if item["name"] == component_name and item["tagType"] == "Folder"),
            None
        )
        if existing_folder is None:
            new_folder = {
                "name": component_name,
                "tagType": "Folder",
                "tags": []
            }
            current_level.append(new_folder)
            current_level = new_folder["tags"]
        else:
            current_level = existing_folder["tags"]

    return current_level

def select_udt_name(instance_name: str) -> str:
    """
    Determines which UDT to use based on the instance_name.

    Parameters:
    - instance_name: The name of the UDT instance.

    Returns:
    - The name of the UDT to use.
    """
    # Check if instance_name is only digits
    if re.fullmatch(r'\d+', instance_name):
        return 'AlarmsDINT'
    # Check if instance_name is text with numbers and does not contain brackets []
    elif re.fullmatch(r'[^\[\]]+', instance_name):
        return 'AlarmsDINT2'
    else:
        # Handle other cases if necessary
        return 'AlarmsDINT'  # Default to 'AlarmsDINT' or raise an error

def prepare_bit_descriptions(instance_df) -> Dict[str, str]:
    """
    Prepares the bit_descriptions dictionary from the instance DataFrame.

    Parameters:
    - instance_df: DataFrame containing data for the instance.

    Returns:
    - A dictionary mapping bit numbers to descriptions.
    """
    return {str(row['Bit']): row['Description'] for _, row in instance_df.iterrows()}

def process_instance(instance_name: str, instance_df, base_udt_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Processes a single UDT instance.

    Parameters:
    - instance_name: The name of the UDT instance.
    - instance_df: DataFrame containing data for the instance.
    - base_udt_data: Dictionary containing loaded UDT JSON data.

    Returns:
    - The UDT instance dictionary ready to be added to the folder structure.
    """
    # Prepare bit descriptions from the instance data
    bit_descriptions = prepare_bit_descriptions(instance_df)

    # Decide which UDT to use based on the instance_name
    udt_name = select_udt_name(instance_name)

    # Make a deep copy of the base UDT tags
    udt_tags = copy.deepcopy(base_udt_data[udt_name]["tags"])

    # Overwrite the UDT tags with bit descriptions
    udt_tags = overwrite_udt_tags(udt_tags, bit_descriptions)

    # Create the UDT instance
    udt_instance = {
        "name": instance_name,
        "typeId": f"AmazonUDTs/AlarmsUDTs/{udt_name}",
        "tagType": "UdtInstance",
        "tags": udt_tags
    }

    return udt_instance

def build_folder_structure(prefix: str, chunk_df, base_udt_data: Dict[str, Any], folder_structure: List[Dict[str, Any]]) -> None:
    """
    Builds the folder structure and inserts UDT instances with overridden values.

    Parameters:
    - prefix: The prefix representing the folder hierarchy.
    - chunk_df: The DataFrame chunk corresponding to the prefix.
    - base_udt_data: Dictionary containing loaded UDT JSON data.
    - folder_structure: The shared folder structure to modify.

    Returns:
    - None
    """
    current_level = build_folder_hierarchy(prefix, folder_structure)

    for instance_name in chunk_df['InstanceName'].unique():
        instance_df = chunk_df[chunk_df['InstanceName'] == instance_name]
        udt_instance = process_instance(instance_name, instance_df, base_udt_data)
        current_level.append(udt_instance)
