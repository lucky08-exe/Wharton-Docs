import yfinance as yf
import pandas as pd
import numpy as np

# Define stock tickers and ETF path

etf_path = 'etflist.xlsx'

# Function to extract ETF tickers from Excel file
def extract_etf_tickers(etf_path):
    etf_data = pd.ExcelFile(etf_path)
    etf_tickers = []
    for sheet1 in etf_data.sheet_names:
        sheet1_data = etf_data.parse(sheet1)
        if 'Ticker' in sheet1_data.columns:
            etf_tickers.extend(sheet1_data['Ticker'].dropna().tolist())
    return list(set(etf_tickers))

etf_tickers = extract_etf_tickers(etf_path)

# Bond data (provided)


# Create DataFrame for bonds
bonds_df = pd.DataFrame(bond_data)

# Download data for stocks and ETFs
stocks_data = yf.download(stock_tickers, start="2022-01-01", end="2023-01-01")
etfs_data = yf.download(etf_tickers, start="2022-01-01", end="2023-01-01")

# Calculate daily returns and mean returns for stocks and ETFs
stock_returns = stocks_data['Adj Close'].pct_change().dropna()
etf_returns = etfs_data['Adj Close'].pct_change().dropna()

# Calculate mean returns for stocks, ETFs, and bonds
mean_stock_returns = stock_returns.mean()
mean_etf_returns = etf_returns.mean()

# Save the results to Excel
with pd.ExcelWriter('investment_returns.xlsx') as writer:
    stock_returns.to_excel(writer, sheet_name='Stock Daily Returns')
    etf_returns.to_excel(writer, sheet_name='ETF Daily Returns')
    mean_stock_returns.to_frame('Mean Stock Returns').to_excel(writer, sheet_name='Mean Stock Returns')
    mean_etf_returns.to_frame('Mean ETF Returns').to_excel(writer, sheet_name='Mean ETF Returns')
    bonds_df.to_excel(writer, sheet_name='Bond Data')

print("Data has been saved to 'investment_returns.xlsx'.")
