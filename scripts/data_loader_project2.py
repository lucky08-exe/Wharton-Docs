import yfinance as yf
import pandas as pd
import numpy as np
from PIL.GimpGradientFile import linear
from yfinance import Ticker


def readFile(file_path, column_name=''):
    df = pd.read_excel(file_path)
    valu = df[column_name].dropna().tolist()
    return valu


def download_data(tickers):
    return yf.download(tickers, start="2020-01-01", end="2024-11-01")['Adj Close']


def clean_data(df):
    # Remove timezone info if present
    if df.index.tz is not None:
        df.index = df.index.tz_localize(None)

    df.interpolate(method="linear")
    return df


lis1 = readFile('valid_tickers.xlsx', 'Ticker')
stocks_list = []
for val in lis1:
    stocks_list.append(str(val))
etfs_list = readFile('valid_etfs.xlsx', 'Ticker')
bondsNames = readFile('valid_bonds.xlsx', 'Bond Name')
bondRates = readFile('valid_bonds.xlsx', 'Rate')

bondDF = pd.DataFrame({
    "Name": bondsNames,
    "Coupon Rate (%)": bondRates,
})
stock_data = clean_data(download_data(stocks_list))
etf_data = clean_data(download_data(etfs_list))

daily_stock_returns = stock_data.pct_change()*100
daily_etf_returns = etf_data.pct_change()*100

mean_stock_returns = daily_stock_returns.mean(axis=0)
mean_etf_returns = daily_etf_returns.mean(axis=0)
finalBondReturns = bondDF['Coupon Rate (%)'].to_numpy().mean(axis=0)

Stocks1 = mean_stock_returns.mean(axis=0)*252
Etfs = mean_etf_returns.mean(axis=0)*252

print(Stocks1)
print(Etfs)
print(finalBondReturns)
