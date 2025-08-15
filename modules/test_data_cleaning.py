import sys
import os

# This line adds the parent directory (your project root) to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import pandas as pd
import numpy as np

from modules import data_cleaning

class TestDataCleaning(unittest.TestCase):

    def setUp(self):
        """This method runs before each test."""
        self.test_df = pd.DataFrame({
            'Product Name': ['Widget A', 'Widget A', 'Gadget B', 'Thingamajig C'],
            'Quantity': [100, 100, 150, np.nan],
            'Price': [10.5, 10.5, 25.0, 5.75]
        })

    def test_standardize_formats(self):
        """Tests if column names are correctly converted to lowercase and have underscores."""
        df_cleaned = data_cleaning.standardize_formats(self.test_df.copy())
        self.assertTrue(all(c.islower() for c in df_cleaned.columns))
        self.assertIn('product_name', df_cleaned.columns) # Check for the final name

    def test_remove_duplicates(self):
        """Tests if duplicate rows are correctly removed."""
        df_cleaned = data_cleaning.remove_duplicates(self.test_df.copy())
        self.assertEqual(len(df_cleaned), 3)

    def test_fill_missing_values(self):
        """Tests if missing values (NaN) are correctly filled."""
        df_filled = data_cleaning.fill_missing_values(self.test_df.copy(), fill_value=0)
        
        # THE FIX IS HERE: We now use the original column name 'Quantity'
        self.assertFalse(df_filled['Quantity'].isnull().any())
        self.assertEqual(df_filled.loc[3, 'Quantity'], 0)

if __name__ == '__main__':
    unittest.main()
