"""
Create a new Santa-Child Excel file with email columns for better verification
"""
import pandas as pd

# Create sample data with usernames and emails
data = {
    'Santa': ['faheem', 'bishal', 'adrija', 'riya'],
    'SantaEmail': ['faheem@deloitte.com', 'bishal@deloitte.com', 'adrija@deloitte.com', 'riya@deloitte.com'],
    'Child': ['farhim', 'adrija', 'riya', 'abhishek'],
    'ChildEmail': ['farhim@deloitte.com', 'adrija@deloitte.com', 'riya@deloitte.com', 'abhishek@deloitte.com']
}

df = pd.DataFrame(data)

# Save to Excel
output_file = 'santa_child_NEW.xlsx'
df.to_excel(output_file, index=False)

print(f"✅ Created {output_file} with the following structure:")
print("\nColumns:")
print("  1. Santa - Username of the gift giver")
print("  2. SantaEmail - Email of the gift giver (for verification)")
print("  3. Child - Username of the gift receiver")
print("  4. ChildEmail - Email of the gift receiver (for verification)")
print(f"\n{len(df)} assignments created")
print("\n📝 Next step: Review the file and rename it to 'santa_child.xlsx' to use it in production")
