import streamlit as st
import pandas as pd
import os

# Import your existing workflow logic
from main import run_workflow, load_config

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Workflow Automation Tool",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Workflow Automation Tool")
st.write("Upload your Excel file to automatically clean, analyze, and visualize your data.")

# --- File Uploader ---
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file is not None:
    st.success(f"File '{uploaded_file.name}' uploaded successfully!")

    # To run your workflow, it needs to save the file temporarily
    input_path = "temp_input.xlsx"
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Define a temporary output path
    output_path = "temp_processed.xlsx"

    # Load config
    config = load_config()

    if config:
        # --- Run Workflow Button ---
        if st.button("✨ Run Analysis", type="primary"):
            with st.spinner("Processing... this might take a moment."):
                run_workflow(input_path, output_path, config)
            
            st.balloons()
            st.success("Workflow completed!")

            # --- Display Results ---
            st.header("Analysis Results")

            # Display the processed data
            st.subheader("Processed Data with Anomaly Flags")
            processed_df = pd.read_excel(output_path)
            st.dataframe(processed_df)

            # Display the generated charts
            st.subheader("Visualizations")
            
            # Check for and display charts
            if os.path.exists("product_quantity.png"):
                st.image("product_quantity.png", caption="Product Quantity Distribution")
            if os.path.exists("price_distribution.png"):
                st.image("price_distribution.png", caption="Price Distribution")
    else:
        st.error("Could not load config.yaml. Please ensure the file is present in the repository.")
