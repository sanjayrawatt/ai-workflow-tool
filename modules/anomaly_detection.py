from sklearn.ensemble import IsolationForest
import pandas as pd

def detect_anomalies(df, columns_to_check):
    """Detects anomalies in specified numeric columns using IsolationForest."""
    # Select only numeric data for the model
    numeric_df = df[columns_to_check].select_dtypes(include=['number'])

    if numeric_df.empty:
        print("Warning: No numeric columns found for anomaly detection. Skipping.")
        return df

    # Initialize and train the model
    model = IsolationForest(contamination='auto', random_state=42)
    predictions = model.fit_predict(numeric_df)

    # Add the results back to the original DataFrame
    # -1 means an anomaly was detected
    df['is_anomaly'] = predictions
    print(f"Anomaly detection complete. Found {df[df['is_anomaly'] == -1].shape[0]} potential anomalies.")
    return df

