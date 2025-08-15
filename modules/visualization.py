import pandas as pd
import matplotlib.pyplot as plt
import os

def create_product_quantity_chart(df, output_folder, filename="product_quantity.png"):
    """
    Creates a bar chart of product quantities and saves it as a PNG image.
    """
    if 'product_name' not in df.columns or 'quantity' not in df.columns:
        print("Warning: DataFrame is missing 'product_name' or 'quantity' for visualization.")
        return

    plt.figure(figsize=(12, 8))
    plt.bar(df['product_name'], df['quantity'], color='skyblue')
    plt.title('Quantity by Product', fontsize=16)
    plt.xlabel('Product Name', fontsize=12)
    plt.ylabel('Quantity', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    full_path = os.path.join(output_folder, filename)
    plt.savefig(full_path)
    plt.close()
    print(f"Chart saved successfully to: {full_path}")


def create_price_distribution_chart(df, output_folder, filename="price_distribution.png"):
    """
    Creates a histogram of the price distribution.
    """
    if 'price' not in df.columns:
        print("Warning: 'price' column missing for price distribution chart.")
        return

    plt.figure(figsize=(10, 6))
    plt.hist(df['price'], bins=15, color='purple', alpha=0.7)
    plt.title('Distribution of Product Prices', fontsize=16)
    plt.xlabel('Price Bins')
    plt.ylabel('Frequency')
    plt.tight_layout()

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    full_path = os.path.join(output_folder, filename)
    plt.savefig(full_path)
    plt.close()
    print(f"Price histogram saved successfully to: {full_path}")
