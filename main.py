import argparse
import pandas as pd
import logging
import os
import yaml

from modules import data_cleaning, validation, anomaly_detection, report_generation, visualization

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("workflow.log", mode='w'),
        logging.StreamHandler()
    ]
)

def load_config(config_path='config.yaml'):
    """Loads the YAML configuration file."""
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logging.error(f"Configuration file not found at {config_path}. Please create it.")
        return None
    except yaml.YAMLError as e:
        logging.error(f"Error parsing the configuration file: {e}")
        return None

def run_workflow(input_path, output_path, config):
    """
    The core data processing logic. This function can be called from any script.
    """
    logging.info(f"--- Starting Workflow ---")
    logging.info(f"Input file: {input_path}")
    logging.info(f"Output file: {output_path}")

    # --- Load Data ---
    try:
        df = pd.read_excel(input_path, engine='openpyxl')
        logging.info("Data loaded successfully.")
    except FileNotFoundError:
        logging.error(f"Error: The file {input_path} was not found. Aborting.")
        return

    # --- Run Processing Steps using Config Values ---
    logging.info("Cleaning data...")
    df = data_cleaning.standardize_formats(df)
    df = data_cleaning.remove_duplicates(df)
    fill_value = config['data_cleaning_settings']['fill_missing_value_with']
    df = data_cleaning.fill_missing_values(df, fill_value=fill_value)
    logging.info("Data cleaning complete.")

    logging.info("Validating data...")
    try:
        required_cols = config['data_validation_settings']['required_columns']
        validation.validate_columns(df, required_columns=required_cols)
    except ValueError as e:
        logging.error(f"Validation Failed: {e}. Aborting.")
        return
    logging.info("Data validation successful.")

    logging.info("Detecting anomalies...")
    numeric_cols = config['anomaly_detection_settings']['columns_for_anomaly_detection']
    df = anomaly_detection.detect_anomalies(df, columns_to_check=numeric_cols)

    # --- Data Visualization ---
    logging.info("Generating data visualizations...")
    output_folder = os.path.dirname(output_path)
    visualization.create_product_quantity_chart(df, output_folder=output_folder)
    visualization.create_price_distribution_chart(df, output_folder=output_folder)

    # --- Generate Report ---
    logging.info(f"Saving processed data...")
    output_filename = os.path.basename(output_path)
    report_generation.save_processed_data(df, output_folder=output_folder, filename=output_filename)
    
    logging.info("--- Workflow Finished Successfully! ---")

def main_cli():
    """
    The main function for the Command-Line Interface (CLI).
    """
    config = load_config()
    if not config:
        return

    parser = argparse.ArgumentParser(description='AI-Powered Workflow Automation Tool')
    parser.add_argument('--input', type=str, default=config['default_input_path'], help='Input Excel file path')
    parser.add_argument('--output', type=str, default=config['default_output_path'], help='Output Excel file path')
    args = parser.parse_args()

    run_workflow(args.input, args.output, config)

if __name__ == "__main__":
    main_cli()
