import yfinance as yf
import numpy as np

# Define the ticker
ticker_symbol = "AAPL"  # Replace with the desired ticker
ticker = yf.Ticker(ticker_symbol)

# Fetch company data
info = ticker.info

# Download historical data
historical_data = yf.download(ticker_symbol, start="2020-01-01", end="2024-11-01")

# Define risk-free rate (annualized, e.g., 2% as 0.02)
risk_free_rate = 0.02


# Function to calculate the required financial metrics for a given ticker
def get_financial_metrics(ticker):
    # Fetch data from Yahoo Finance
    stock = yf.Ticker(ticker)

    # Get financials
    financials = stock.financials
    balance_sheet = stock.balance_sheet
    cashflow = stock.cashflow

    # Extract metrics
    eps = stock.info.get('epsTrailingTwelveMonths')
    gross_profit = financials.loc['Gross Profit'].iloc[0] if 'Gross Profit' in financials.index else None
    revenue = financials.loc['Total Revenue'].iloc[0] if 'Total Revenue' in financials.index else None
    net_income = financials.loc['Net Income'].iloc[0] if 'Net Income' in financials.index else None

    # Gross Profit Margin
    gross_profit_margin = gross_profit / revenue * 100 if revenue != 0 else None

    # Profit Margin
    profit_margin = net_income / revenue * 100 if revenue != 0 else None

    total_assets = balance_sheet.loc['Total Assets'].iloc[0] if 'Total Assets' in balance_sheet.index else None
    free_cash_flow = cashflow.loc['Free Cash Flow'].iloc[0] if 'Free Cash Flow' in cashflow.index else None

    # Print the results
    print(f"Financial Metrics for {ticker}:")
    print(f"EPS (Trailing Twelve Months): {eps}")
    print(f"Gross Profit Margin: {gross_profit_margin:.2f}%" if gross_profit_margin else "Gross Profit Margin: N/A")
    print(f"Profit Margin: {profit_margin:.2f}%" if profit_margin else "Profit Margin: N/A")
    print(f"Total Assets: {total_assets}")
    print(f"Free Cash Flow: {free_cash_flow}")

    return {
        "EPS": eps,
        "Gross Profit Margin": gross_profit_margin,
        "Profit Margin": profit_margin,
        "Total Assets": total_assets,
        "Free Cash Flow": free_cash_flow
    }


# Function to calculate financial ratios
def calculate_ratios(info, historical_data):
    ratios = {}

    # Ensure historical data includes 'Adj Close'
    if 'Adj Close' in historical_data:
        # Calculate daily returns
        historical_data['Returns'] = historical_data['Adj Close'].pct_change()
        daily_returns = historical_data['Returns'].dropna()

        # Annualized Return
        annualized_return = (1 + daily_returns.mean()) ** 252 - 1
        ratios['Annualized_Return'] = annualized_return

        # Annualized Volatility
        annualized_volatility = daily_returns.std() * np.sqrt(252)
        ratios['Annualized_Volatility'] = annualized_volatility

        # Sharpe Ratio
        if annualized_volatility > 0:
            ratios['Sharpe_Ratio'] = (annualized_return - risk_free_rate) / annualized_volatility

        # Sortino Ratio
        downside_returns = daily_returns[daily_returns < 0]
        if len(downside_returns) > 0:
            downside_deviation = downside_returns.std() * np.sqrt(252)
            ratios['Sortino_Ratio'] = (annualized_return - risk_free_rate) / downside_deviation

        # Maximum Drawdown
        cumulative_returns = (1 + daily_returns).cumprod()
        peak = cumulative_returns.cummax()
        drawdown = (cumulative_returns - peak) / peak
        max_drawdown = drawdown.min()
        ratios['Max_Drawdown'] = max_drawdown

    # P/E Ratio
    if 'trailingEps' in info and info.get('trailingEps') and 'currentPrice' in info:
        ratios['PE_Ratio'] = info['currentPrice'] / info['trailingEps']

    # P/B Ratio
    if 'bookValue' in info and info.get('bookValue') and 'currentPrice' in info:
        ratios['PB_Ratio'] = info['currentPrice'] / info['bookValue']

    # Dividend Yield
    if 'dividendRate' in info and info.get('dividendRate') and 'currentPrice' in info:
        ratios['Dividend_Yield'] = info['dividendRate'] / info['currentPrice']

    # EV/Revenue Ratio
    if 'enterpriseValue' in info and info.get('enterpriseValue') and 'totalRevenue' in info:
        ratios['EV_to_Revenue'] = info['enterpriseValue'] / info['totalRevenue']

    # Debt-to-Equity Ratio
    if 'totalDebt' in info and info.get('totalDebt') and 'bookValue' in info:
        ratios['Debt_to_Equity'] = info['totalDebt'] / (info['bookValue'] * info['sharesOutstanding'])
        print(info.get())

    return ratios


# Get financial metrics
metrics = get_financial_metrics(ticker_symbol)

# Calculate financial ratios
financial_ratios = calculate_ratios(info, historical_data)

# Print results
print("\nFinancial Ratios:")
for ratio, value in financial_ratios.items():
    print(f"{ratio}: {value:.4f}" if isinstance(value, (int, float)) else f"{ratio}: {value}")
