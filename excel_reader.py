"""
Module to read Secret Santa assignments from Excel file
"""
import pandas as pd
import os

def get_assignment_from_excel(santa_email):
    """
    Read Excel file and get the child assignment based on Santa's email
    
    Args:
        santa_email: The email of the Santa (giver)
        
    Returns:
        dict with child_email if found, None otherwise
    """
    try:
        excel_file = 'santa_child.xlsx'
        
        if not os.path.exists(excel_file):
            print(f"Error: {excel_file} not found")
            return None
        
        # Read the Excel file
        df = pd.read_excel(excel_file)
        
        # Check if required email columns exist
        required_columns = ['SantaEmail', 'ChildEmail', 'ChildName']
        if not all(col in df.columns for col in required_columns):
            print(f"Error: Excel must have {required_columns} columns")
            return None
        
        # Normalize the email for comparison
        santa_email = santa_email.strip().lower()
        
        # Find the row where SantaEmail matches (case-insensitive)
        matching_rows = df[df['SantaEmail'].str.lower().str.strip() == santa_email]
        
        if len(matching_rows) > 0:
            row = matching_rows.iloc[0]
            
            result = {
                'child_email': str(row['ChildEmail']).strip().lower(),
                'child_name': str(row['ChildName']).strip()
            }
            return result
        
        print(f"No assignment found for email: {santa_email}")
        return None
        
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None

def get_all_child_names_from_excel():
    """Get all unique child names from Excel file for spinner wheel"""
    try:
        excel_file = 'santa_child.xlsx'
        
        if not os.path.exists(excel_file):
            return []
        
        df = pd.read_excel(excel_file)
        
        if 'ChildName' not in df.columns:
            return []
        
        # Get all unique child names
        child_names = df['ChildName'].dropna().unique().tolist()
        # Clean and return
        return [str(name).strip() for name in child_names]
        
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return []

def get_santa_name_by_email(santa_email):
    """Get Santa's name from Excel based on their email"""
    try:
        excel_file = 'santa_child.xlsx'
        
        if not os.path.exists(excel_file):
            return None
        
        df = pd.read_excel(excel_file)
        
        if 'SantaEmail' not in df.columns or 'SantaName' not in df.columns:
            return None
        
        # Normalize email for comparison
        santa_email = santa_email.strip().lower()
        
        # Find matching row
        matching_rows = df[df['SantaEmail'].str.lower().str.strip() == santa_email]
        
        if len(matching_rows) > 0:
            return str(matching_rows.iloc[0]['SantaName']).strip()
        
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
        
        # Check if email columns exist
        has_emails = 'SantaEmail' in df.columns and 'ChildEmail' in df.columns
        
        assignments = []
        for _, row in df.iterrows():
            assignment = {
                'santa': str(row['Santa']).strip(),
                'child': str(row['Child']).strip()
            }
            
            if has_emails:
                assignment['santa_email'] = str(row['SantaEmail']).strip() if pd.notna(row.get('SantaEmail')) else None
                assignment['child_email'] = str(row['ChildEmail']).strip() if pd.notna(row.get('ChildEmail')) else None
            
            assignments.append(assignment)
        
        return assignments
        
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return []
