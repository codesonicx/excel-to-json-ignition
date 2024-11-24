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

def extract_instance_name(df):
    """Extracts the 'InstanceName' from the 'Tag' column."""
    # df["InstanceName"] = df["Tag"].apply(
    #     lambda x: re.search(r"\[(.*?)\]", x).group(1)
    #     if "[" in x and "]" in x
    #     else x.split(".")[-2]
    # )
    df["InstanceName"] = df["Tag"].apply(
        lambda x: re.search(r"\]\.(\w+)", x).group(1) 
        if re.search(r"\]\.(\w+)", x)
        else x.split(".")[-2]
    )
    return df

def extract_bit(df):
    """Extracts the 'Bit' from the 'Tag' column."""
    df["Bit"] = df["Tag"].apply(lambda x: x.split(".")[-1])
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
    df = extract_prefix(df)
    df = process_prefix(df)
    df = extract_instance_name(df)
    df = extract_bit(df)
    df = drop_columns(df)
    df = reorder_columns(df)
    return df
