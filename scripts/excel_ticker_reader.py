import pandas as pd

# Replace 'your_file.xlsx' with the path to your Excel file and 'Sheet1' with the appropriate sheet name
file_path = 'FINAL 24-25 Approved Stock List.xlsx'
sheet_name = 'Sheet1'

# Read the Excel file
df = pd.read_excel(file_path, sheet_name=sheet_name)

# Assuming column 'C' corresponds to the third column (0-indexed)
# Adjust the column name as necessary, e.g., df['ColumnCName'] if the column has a header
names = df.iloc[:, 2].tolist()  # Read column C (third column)

# Remove duplicates by converting the list to a set and back to a list
unique_names = list(set(names))

# Sort the list if desired (optional)
unique_names.sort()

# Print the unique names
print(unique_names)
