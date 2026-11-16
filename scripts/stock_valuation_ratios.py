import yfinance as yf
import pandas as pd

ticker = 'AAPL'
stock = yf.Ticker(ticker)


current_price = stock.history(period='1d')['Close'].iloc[-1]

info = stock.info
net_income = info.get('netIncome', 0)  # in dollars
shares_outstanding = info.get('sharesOutstanding', 0)  # total shares

eps = net_income / shares_outstanding
pe_ratio = current_price / eps


print(f"Stock: {ticker}")
print(f"Current Price: ${current_price:.2f}")
print(f"Earnings Per Share (EPS): ${eps:.2f}")
print(f"P/E Ratio: {pe_ratio:.2f}")
