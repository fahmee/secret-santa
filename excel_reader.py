"""
Module to read Secret Santa assignments from Excel file
"""
import pandas as pd
import os

def get_assignment_from_excel(santa_username):
    """
    Read Excel file and get the child for a given Santa
    
    Args:
        santa_username: The username of the Santa (giver)
        
    Returns:
        child_username if found, None otherwise
    """
    try:
        excel_file = 'santa_child.xlsx'
        
        if not os.path.exists(excel_file):
            print(f"Error: {excel_file} not found")
            return None
        
        # Read the Excel file
        df = pd.read_excel(excel_file)
        
        # Check if required columns exist
        if 'Santa' not in df.columns or 'Child' not in df.columns:
            print("Error: Excel must have 'Santa' and 'Child' columns")
            return None
        
        # Find the row where Santa matches the username (case-insensitive)
        matching_rows = df[df['Santa'].str.lower() == santa_username.lower()]
        
        if len(matching_rows) > 0:
            child = matching_rows.iloc[0]['Child']
            return str(child).strip()
        
        return None
        
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None

def get_all_assignments_from_excel():
    """Get all Santa-Child pairs from Excel"""
    try:
        excel_file = 'santa_child.xlsx'
        
        if not os.path.exists(excel_file):
            return []
        
        df = pd.read_excel(excel_file)
        
        assignments = []
        for _, row in df.iterrows():
            assignments.append({
                'santa': str(row['Santa']).strip(),
                'child': str(row['Child']).strip()
            })
        
        return assignments
        
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return []
