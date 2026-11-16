

import pandas as pd

# Dictionary mapping stock exchanges to their respective countries
exchange_to_country = {
    'B3 S.A.': 'Brazil',
    'BMV': 'Mexico',
    'BSE LTD': 'India',
    'Euronext': 'Amsterdam',
    'Frankfurt Stock Exchange': 'Germany',
    'Ho Chi Minh Stock Exchange': 'Vietnam',
    'Hong Kong Exchanges And Clearing Ltd': 'Hong Kong',
    'Korea Exchange': 'Korea',
    'London Stock Exchange': 'UK',
    'Nasdaq': 'USA',
    'New York Stock Exchange, Inc.': 'USA',
    'SIX Swiss Exchange': 'Switzerland',
    'Shanghai Stock Exchange': 'China',
    'Shenzhen Stock Exchange': 'China',
    'Toronto Stock Exchange': 'Canada'
}

# Load the stock file
file_path = 'stocksfile.xlsx'  # Replace with your actual file path
df = pd.read_excel(file_path)

# Assuming Column C has the stock exchanges
# Replace 'Column C' with the actual name or index of your column if it has a header
df['Country'] = df.iloc[:, 2].map(exchange_to_country)  # Assuming Column C is the third column

# Create a new Excel writer object
output_file = 'countries_stock_data.xlsx'
with pd.ExcelWriter(output_file) as writer:
    # Loop through the mapping dictionary and filter rows for each country
    countries_exchanges = {}
    for exchange, country in exchange_to_country.items():
        if country not in countries_exchanges:
            countries_exchanges[country] = []
        countries_exchanges[country].append(exchange)

    for country, exchanges in countries_exchanges.items():
        # Filter the DataFrame for rows that match any of the exchanges for the current country
        country_data = df[df.iloc[:, 2].isin(exchanges)]  # Adjust based on your column structure
        if not country_data.empty:
            # Write the filtered data to a new sheet named after the country
            country_data.to_excel(writer, sheet_name=country, index=False)

print(f"Excel file '{output_file}' created with sheets for each country.")
