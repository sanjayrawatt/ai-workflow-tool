import pandas as pd
import os

def save_processed_data(df, output_folder, filename="processed_data.xlsx"):
    """
    Saves the processed DataFrame to an Excel file.
    """
    # NOTE: We no longer create a directory. We just save to the path provided.
    full_path = os.path.join(output_folder, filename)
    df.to_excel(full_path, index=False, engine='openpyxl')
    print(f"Successfully saved processed data to: {full_path}")
