"""Script to read and display Excel file structure"""
import pandas as pd

try:
    df = pd.read_excel('santa_child.xlsx')
    print("Excel file loaded successfully!")
    print(f"\nColumns: {list(df.columns)}")
    print(f"\nTotal rows: {len(df)}")
    print("\nFirst few rows:")
    print(df.head())
except Exception as e:
    print(f"Error reading Excel: {e}")
