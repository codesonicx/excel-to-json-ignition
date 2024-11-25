from excel_processor_new import process_excel
from data_grouper import group_by_prefix
from load_udt_json_files import load_base_udt_data
from folder_structure_builder import build_folder_structure
from json_writer import write_json_to_file

# Step 1: Process the Excel file
file_path = r"data\input\Alarms.xlsx"
df = process_excel(file_path)

# Step 2: Group the DataFrame by 'Prefix'
grouped_chunks = group_by_prefix(df)

# Step 3: Load base UDT JSON files once
file_paths = [
    r"data\raw\UDTs\AlarmsDINT.json",
    r"data\raw\UDTs\AlarmsDINT2.json"
    ]
base_udt_data = load_base_udt_data(file_paths)

# Initialize the folder structure
folder_structure = []

# Step 4: Build the folder structure incrementally
for prefix, chunk_df in grouped_chunks.items():
    print(f"Processing prefix: {prefix}")
    build_folder_structure(prefix, chunk_df, base_udt_data, folder_structure)

# Step 5: Write the final JSON to a file
output_json_path = r"data\output\folder_structure.json"
write_json_to_file(folder_structure, output_json_path)

print(f"Folder structure generated correctly in {output_json_path}")
