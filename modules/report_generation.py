import pandas as pd
import os

def save_processed_data(df, output_folder, filename="processed_data.xlsx"):
    """Saves the final DataFrame to an Excel file in the specified folder."""
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    full_path = os.path.join(output_folder, filename)
    df.to_excel(full_path, index=False)
    print(f"Successfully saved processed data to: {full_path}")

