import yfinance as yf
import pandas as pd
import numpy as np


def readStocks(file_path, sheet_name=0, column_name='Ticker'):
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    tickers = df[column_name].dropna().tolist()  # Convert to a list after dropping NaNs
    return tickers


def readETF(file_path, sheet_name=0, column_name='Ticker'):
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    etf = df[column_name].dropna().tolist()  # Convert to a list after dropping NaNs
    return etf


def readBonds(file_path, sheet_name=0, column_name='Coupon Rate'):
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    bonds = df[column_name].dropna().tolist()  # Convert to a list after dropping NaNs
    return bonds


def download_data(tickers):
    return yf.download(tickers, start="2020-01-01", end="2024-11-01")['Adj Close']


def clean_data(df):
    # Remove timezone info if present
    if df.index.tz is not None:
        df.index = df.index.tz_localize(None)  # Remove timezone information from the index

    df = df.replace(0, np.nan)  # Replace zeros with NaN
    df = df.interpolate(method='linear', limit_direction='both', axis=0)  # Interpolate missing values
    return df


stocks_list = readStocks('valid_tickers.xlsx')
etfs_list = readETF('valid_etfs.xlsx')
bondsReturnRates = readBonds('valid_bonds.xlsx')

stock_data = clean_data(download_data(stocks_list))
etf_data = clean_data(download_data(etfs_list))

daily_stock_returns = stock_data.pct_change()*100
daily_etf_returns = etf_data.pct_change()*100

mean_stock_returns = daily_stock_returns.mean(axis=0).tolist()
mean_etf_returns = daily_etf_returns.mean(axis=0).tolist()

finalStockMean = np.mean(mean_stock_returns)*252
finalEtfMean = np.mean(mean_etf_returns)*252

print(finalStockMean)
print(finalEtfMean)

# Write data to Excel
with pd.ExcelWriter('investment_returns.xlsx') as writer:
    daily_stock_returns.to_excel(writer, sheet_name='Daily Stock Returns')
    daily_etf_returns.to_excel(writer, sheet_name='Daily ETF Returns')
    pd.DataFrame({'Mean Stock Returns': mean_stock_returns}).to_excel(writer, sheet_name='Mean Stock Returns', index=False)
    pd.DataFrame({'Mean ETF Returns': mean_etf_returns}).to_excel(writer, sheet_name='Mean ETF Returns', index=False)


