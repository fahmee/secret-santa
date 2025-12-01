"""
Module to read Secret Santa assignments from Excel file
"""
import pandas as pd
import os

def get_assignment_from_excel(santa_username, santa_email=None):
    """
    Read Excel file and get the child for a given Santa
    
    Args:
        santa_username: The username of the Santa (giver)
        santa_email: Optional email to verify the Santa (for added security)
        
    Returns:
        dict with child_username and child_email if found, None otherwise
    """
    try:
        excel_file = 'santa_child.xlsx'
        
        if not os.path.exists(excel_file):
            print(f"Error: {excel_file} not found")
            return None
        
        # Read the Excel file
        df = pd.read_excel(excel_file)
        
        # Check if required columns exist
        required_columns = ['Santa', 'Child']
        if not all(col in df.columns for col in required_columns):
            print("Error: Excel must have 'Santa' and 'Child' columns")
            return None
        
        # Check if email columns exist (optional but recommended)
        has_emails = 'SantaEmail' in df.columns and 'ChildEmail' in df.columns
        
        # Find the row where Santa matches the username (case-insensitive)
        matching_rows = df[df['Santa'].str.lower() == santa_username.lower()]
        
        if len(matching_rows) > 0:
            row = matching_rows.iloc[0]
            
            # If email verification is enabled and email is provided
            if has_emails and santa_email:
                santa_email_from_excel = str(row['SantaEmail']).strip().lower()
                if santa_email.lower() != santa_email_from_excel:
                    print(f"Warning: Email mismatch for user {santa_username}")
                    return None
            
            result = {
                'child_username': str(row['Child']).strip(),
                'child_email': str(row['ChildEmail']).strip() if has_emails and pd.notna(row.get('ChildEmail')) else None
            }
            return result
        
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
