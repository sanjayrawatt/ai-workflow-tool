import pandas as pd

def validate_columns(df, required_columns):
    """Checks if all required columns are present in the DataFrame."""
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        # If columns are missing, stop the process by raising an error
        raise ValueError(f"Validation Failed: Missing required columns: {missing_columns}")
    print("Columns validated successfully.")
    return True

