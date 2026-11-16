import yfinance as yf
import pandas as pd

df = pd.read_excel("valid_tickers.xlsx")
tickers = df['Ticker'].dropna().tolist()
l1 = []

for ticker in tickers:
    stock = yf.Ticker(ticker)
    OM = stock.info.get('operatingMargins', 0) * 100 if stock.info.get('operatingMargins') is not None else 0
    ROA = stock.info.get('returnOnAssets', 0) * 100 if stock.info.get('returnOnAssets') is not None else 0
    EPS = stock.info.get('trailingEps', 0) if stock.info.get('trailingEps') is not None else 0
    RG = stock.info.get('revenueGrowth', 0) * 100 if stock.info.get('revenueGrowth') is not None else 0
    NPM = stock.info.get('profitMargins', 0) * 100 if stock.info.get('profitMargins') is not None else 0

    if OM > 10 and NPM > 10 and ROA > 5 and RG > 5 and EPS > 0:
        l1.append(ticker)
        print("added one")

for t in l1:
    print(t)
