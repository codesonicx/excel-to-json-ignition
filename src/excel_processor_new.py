import pandas as pd
import re

def read_excel(file_path):
    """Reads the Excel file and assigns column names."""
    return pd.read_excel(file_path, header=None, names=["Tag", "Description"])

def clean_data(df):
    """Cleans the data by replacing 'N/A' and dropping rows with null 'Tag'."""
    df = df.replace("N/A", pd.NA).dropna(subset=["Tag"]).reset_index(drop=True)
    return df

def remove_wildcard_rows(df):
    """Removes rows where the value after the last dot in 'Tag' is '*'."""
    return df[~df["Tag"].str.split(".").str[-1].str.contains(r"^\*$")].reset_index(drop=True)

def extract_prefix(df):
    """Extracts the initial prefix from the 'Tag' column."""
    df['Prefix'] = df['Tag'].str.rsplit(pat='.', n=1).str[0]
    df['Prefix_last_part'] = df['Prefix'].str.rsplit(pat='.', n=1).str[-1]
    return df

def process_prefix(df):
    """Processes the prefix to clean or adjust based on square brackets."""
    mask = df['Prefix_last_part'].str.contains(r'\[.*?\]')
    df.loc[mask, 'Prefix_last_part'] = df.loc[mask, 'Prefix_last_part'].str.replace(r'\[.*?\]', '', regex=True)
    df.loc[mask, 'Prefix'] = df.loc[mask, 'Prefix'].str.rsplit(pat='.', n=1).str[0] + '.' + df.loc[mask, 'Prefix_last_part']
    df.loc[~mask, 'Prefix'] = df.loc[~mask, 'Prefix'].str.rsplit(pat='.', n=1).str[0]
    return df.drop(columns=['Prefix_last_part'])

def extract_instance_name_and_prefix(df):
    """Extracts InstanceName and Prefix using the helper column."""
    def extract_details(tag_helper):
        if "[" in tag_helper and "]" in tag_helper:
            # Si hay corchetes, separa el Prefix y el InstanceName.
            prefix = tag_helper.split("[")[0]  # Antes del primer corchete.
            instance_name = re.search(r"\[(.*?)\]", tag_helper).group(1)  # Dentro de los corchetes.
        else:
            # Si no hay corchetes, usa el último punto como separador.
            prefix = ".".join(tag_helper.split(".")[:-1])  # Todo excepto el último elemento.
            instance_name = tag_helper.split(".")[-1]  # Última parte como InstanceName.
        return prefix, instance_name

    # Aplica la extracción a cada fila.
    df[["Prefix", "InstanceName"]] = df["Tag_Helper"].apply(lambda x: pd.Series(extract_details(x)))

    # Elimina la columna auxiliar Tag_Helper.
    return df.drop(columns=["Tag_Helper"])

def extract_bit_number(df):
    """Extracts the Bit number and creates a helper column for the remaining string."""
    df["Bit"] = df["Tag"].apply(lambda x: x.split(".")[-1] if x.split(".")[-1].isdigit() else None)
    df["Tag_Helper"] = df["Tag"].apply(lambda x: ".".join(x.split(".")[:-1]))  # Elimina el Bit number del Tag.
    return df

def drop_columns(df):
    """Drops unnecessary columns after processing."""
    return df.drop(columns=["Tag"])

def reorder_columns(df):
    """Reorders the columns in the DataFrame."""
    return df[["Prefix", "InstanceName", "Bit", "Description"]]

def process_excel(file_path):
    """Main function to process the Excel file and return a cleaned DataFrame."""
    df = read_excel(file_path)
    df = clean_data(df)
    df = remove_wildcard_rows(df)
    
    # Extraer el bit number y actualizar el Tag.
    df = extract_bit_number(df)
    
    # Extraer InstanceName y Prefix del Tag simplificado.
    df = extract_instance_name_and_prefix(df)
    
    # Reordenar las columnas para la salida final.
    df = reorder_columns(df)
    return df
