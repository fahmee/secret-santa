import pandas as pd
from excel_reader import get_assignment_from_excel

# Read and display Excel structure
df = pd.read_excel('santa_child.xlsx')
print("Columns:", df.columns.tolist())
print("\nAll data:")
print(df.to_string())

# Test the function
print("\n\n--- Testing get_assignment_from_excel ---")
result = get_assignment_from_excel('fahahmad@deloitte.com')
print(f"\nResult for fahahmad@deloitte.com: {result}")
