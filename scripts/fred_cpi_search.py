import pandas as pd
from fredapi import Fred

# Set up FRED API Key
api_key = 'your_fred_api_key_here'  # Replace with your actual FRED API key
fred = Fred(api_key=api_key)

# Search for data series related to "Australia CPI"
search_results = fred.search("Australia CPI")

# Set display options to show the full content of all columns without truncation
pd.set_option('display.max_columns', None)    # Display all columns
pd.set_option('display.max_rows', None)       # Display all rows
pd.set_option('display.max_colwidth', None)   # Display full content in each cell

# Print the entire DataFrame content including full 'notes'
print(search_results.to_string(index=False))
