import yfinance as yf
import pandas as pd
import statsmodels.api as sm
from fredapi import Fred

# Define your FRED API key
fred_api_key = "your_fred_api_key_here"  # Replace with your FRED API key
fred = Fred(api_key=fred_api_key)

# Fetch macroeconomic data from FRED
# Consumer Price Index (CPI) for inflation
inflation = fred.get_series('CPIAUCSL')

# Real GDP growth rate (A191RL1Q225SBEA is the code for GDP growth)
gdp_growth = fred.get_series('A191RL1Q225SBEA')

# Federal Funds Rate (interest rate)
interest_rate = fred.get_series('FEDFUNDS')

# Fetch stock data for the S&P 500 Index (symbol: ^GSPC for USA)
stock_data = yf.download('^GSPC', start="2000-01-01", end="2024-01-01")

# Use Adjusted Close price for stock price (this accounts for splits, dividends, etc.)
stock_data['stock_price'] = stock_data['Adj Close']

# Resample stock data to monthly frequency and use the last available data point for each month
stock_data = stock_data[['stock_price']].resample('ME').last()

# Remove timezone information from stock_data index
stock_data.index = stock_data.index.tz_localize(None)

# Merge the macroeconomic data with stock price data (ensure dates match)
df = pd.DataFrame({
    'stock_price': stock_data['stock_price'],
    'inflation': inflation.resample('ME').last(),
    'gdp_growth': gdp_growth.resample('ME').last(),
    'interest_rate': interest_rate.resample('ME').last()
})

# Drop rows with missing values (if any data is missing for a particular month)
df.dropna(inplace=True)

# Define the independent variables (macroeconomic data)
X = df[['inflation', 'gdp_growth', 'interest_rate']]
X = sm.add_constant(X)  # Add a constant term (intercept)

# Define the dependent variable (stock price)
Y = df['stock_price']

# Perform Ordinary Least Squares (OLS) regression
model = sm.OLS(Y, X).fit()

# Print the summary of the regression model
print(model.summary())
