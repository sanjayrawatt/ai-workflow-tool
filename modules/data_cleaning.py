# In modules/data_cleaning.py

import pandas as pd

def standardize_formats(df):
    """
    Converts all column names to lowercase and replaces spaces with underscores.
    """
    # This is the corrected line
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    return df

def remove_duplicates(df):
    return df.drop_duplicates()

def fill_missing_values(df, fill_value=0):
    return df.fillna(fill_value)
