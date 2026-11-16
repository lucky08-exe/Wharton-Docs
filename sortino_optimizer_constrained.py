import yfinance as yf
import pandas as pd
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from statsmodels.genmod.families.varfuncs import constant

MAR = 10.06


def readFile(file_path, column_name=''):
    df = pd.read_excel(file_path)
    valu = df[column_name].dropna().tolist()  # Convert to a list after dropping NaNs
    return valu


def download_data(tickers):
    return yf.download(tickers, start="2020-01-01", end="2024-11-01")['Adj Close']


def clean_data(df):
    # Remove timezone info if present
    if df.index.tz is not None:
        df.index = df.index.tz_localize(None)

    df.interpolate(method="linear", inplace=True)
    return df


# Reading ticker data
lis1 = readFile('valid_tickers.xlsx', 'Ticker')
stocks_list = [str(val) for val in lis1]
etfs_list = readFile('valid_etfs.xlsx', 'Ticker')
bondsNames = readFile('valid_bonds.xlsx', 'Bond Name')
bondRates = readFile('valid_bonds.xlsx', 'Rate')

bondDF = pd.DataFrame({
    "Name": bondsNames,
    "Coupon Rate (%)": bondRates,
})

# Download and clean data for stocks and ETFs
stock_data = clean_data(download_data(stocks_list))
etf_data = clean_data(download_data(etfs_list))

# Calculate daily returns (percentage change)
daily_stock_returns = stock_data.pct_change() * 100
daily_etf_returns = etf_data.pct_change() * 100

# Calculate the mean returns
mean_stock_returns = daily_stock_returns.mean(axis=0)
mean_etf_returns = daily_etf_returns.mean(axis=0)

finalStockReturns = np.array(mean_stock_returns) * 252
finalEtfReturns = np.array(mean_etf_returns) * 252
finalBondReturns = np.array(bondDF['Coupon Rate (%)'])

max_length = max(len(finalStockReturns), len(finalEtfReturns), len(finalBondReturns))

# Pad the shorter arrays with NaNs to match the maximum length
finalStockReturns = np.pad(finalStockReturns, (0, max_length - len(finalStockReturns)), mode='constant', constant_values=np.nan)
finalEtfReturns = np.pad(finalEtfReturns, (0, max_length - len(finalEtfReturns)), mode='constant', constant_values=np.nan)
finalBondReturns = np.pad(finalBondReturns, (0, max_length - len(finalBondReturns)), mode='constant', constant_values=np.nan)

# Stack the arrays vertically
all_asset_returns = np.vstack([finalStockReturns, finalEtfReturns, finalBondReturns])



def portfolio_return(weights, asset_returns):
    return np.dot(weights, np.mean(asset_returns, axis=1))


# Function to calculate portfolio downside deviation
def downside_deviation(weights, asset_returns, MAR):
    portfolio_returns = np.dot(asset_returns.T, weights)
    downside = np.minimum(0, portfolio_returns - MAR)  # Only consider returns below MAR
    return np.sqrt(np.mean(downside ** 2))  # Downside deviation (semi-variance)


# Function to calculate the Sortino ratio
def sortino_ratio(weights, asset_returns, MAR, rf_rate=0.0):
    port_return = portfolio_return(weights, asset_returns) - rf_rate
    port_downside = downside_deviation(weights, asset_returns, MAR)
    return port_return / port_downside if port_downside != 0 else np.nan


# Objective: Maximize Sortino Ratio (minimize negative Sortino ratio)
def sortino_maximizer(weights, asset_returns, MAR):
    return -sortino_ratio(weights, asset_returns, MAR)


# Constraints: Weights sum to 1
constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1}]
# Bounds: No short-selling (weights between 0 and 1)
num_assets = all_asset_returns.shape[0]
bounds = [(0, 1) for _ in range(num_assets)]

# Initial guess: Equal weights
initial_weights = np.ones(num_assets) / num_assets

# Optimization
opt_results = minimize(sortino_maximizer, initial_weights,
                       args=(all_asset_returns, MAR),
                       bounds=bounds,
                       constraints=constraints)

optimal_weights = opt_results.x
optimal_return = portfolio_return(optimal_weights, all_asset_returns)
optimal_downside = downside_deviation(optimal_weights, all_asset_returns, MAR)
optimal_sortino = -opt_results.fun

# Print results
print("Optimal Weights:", optimal_weights)
print("Optimal Portfolio Return:", optimal_return)
print("Optimal Portfolio Downside Deviation:", optimal_downside)
print("Optimal Sortino Ratio:", optimal_sortino)


# Generate points along the efficient frontier
portfolio_downsides = []
portfolio_returns = []

# You can loop through weights directly
weight_combinations = np.linspace(0, 1, 100)
for w1 in weight_combinations:
    for w2 in weight_combinations:
        w3 = 1 - w1 - w2
        if w3 >= 0:  # Ensure weights sum to 1
            weights = np.array([w1, w2, w3])
            portfolio_downsides.append(downside_deviation(weights, all_asset_returns, MAR))
            portfolio_returns.append(portfolio_return(weights, all_asset_returns))

# Convert to numpy arrays for plotting
portfolio_downsides = np.array(portfolio_downsides)
portfolio_returns = np.array(portfolio_returns)

# Plot the efficient frontier
plt.figure(figsize=(10, 6))
plt.scatter(portfolio_downsides, portfolio_returns, c=portfolio_returns / portfolio_downsides, cmap='viridis', alpha=0.6)
plt.colorbar(label="Sortino Ratio")
plt.scatter(optimal_downside, optimal_return, color='red', label="Optimal Portfolio", s=50)
plt.axvline(x=MAR, color='black', linestyle='--', label="Maximum Acceptable Risk (MAR)")
plt.title("PMPT Efficient Frontier for Three Assets")
plt.xlabel("Downside Deviation (Risk)")
plt.ylabel("Expected Return")
plt.legend()
plt.show()


