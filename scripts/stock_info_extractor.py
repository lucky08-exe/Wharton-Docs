import yfinance as yf

# Fetch data for AAPL
ticker = 'AAPL'
stock = yf.Ticker(ticker)

# Get the relevant data
data = {
    # Ratios
    'quickRatio': stock.info.get('quickRatio'),
    'currentRatio': stock.info.get('currentRatio'),
    'debtToEquity': stock.info.get('debtToEquity'),
    'returnOnAssets': stock.info.get('returnOnAssets'),
    'returnOnEquity': stock.info.get('returnOnEquity'),
    'earningsGrowth': stock.info.get('earningsGrowth'),
    'revenueGrowth': stock.info.get('revenueGrowth'),
    'grossMargins': stock.info.get('grossMargins'),
    'priceToBook': stock.info.get('priceToBook'),
    'priceToSalesTrailing12Months': stock.info.get('priceToSalesTrailing12Months'),
    'trailingPE': stock.info.get('trailingPE'),
    'forwardPE': stock.info.get('forwardPE'),
    'priceToSalesTrailing12Months': stock.info.get('priceToSalesTrailing12Months'),
    'priceHint': stock.info.get('priceHint'),
    'beta': stock.info.get('beta'),

    # 52-Week Data
    '52WeekChange': stock.info.get('52WeekChange'),
    'fiftyTwoWeekLow': stock.info.get('fiftyTwoWeekLow'),
    'fiftyTwoWeekHigh': stock.info.get('fiftyTwoWeekHigh'),

    # Dividend Info
    'lastDividendValue': stock.info.get('lastDividendValue'),
    'lastDividendDate': stock.info.get('lastDividendDate'),
    'dividendRate': stock.info.get('dividendRate'),
    'dividendYield': stock.info.get('dividendYield'),
    'exDividendDate': stock.info.get('exDividendDate'),
    'payoutRatio': stock.info.get('payoutRatio'),
    'fiveYearAvgDividendYield': stock.info.get('fiveYearAvgDividendYield'),
    'trailingAnnualDividendRate': stock.info.get('trailingAnnualDividendRate'),
    'trailingAnnualDividendYield': stock.info.get('trailingAnnualDividendYield'),

    # Price Data
    'currentPrice': stock.info.get('currentPrice'),
    'previousClose': stock.info.get('previousClose'),
    'open': stock.info.get('open'),
    'dayLow': stock.info.get('dayLow'),
    'dayHigh': stock.info.get('dayHigh'),
    'regularMarketPreviousClose': stock.info.get('regularMarketPreviousClose'),
    'regularMarketOpen': stock.info.get('regularMarketOpen'),
    'regularMarketDayLow': stock.info.get('regularMarketDayLow'),
    'regularMarketDayHigh': stock.info.get('regularMarketDayHigh'),
    'targetHighPrice': stock.info.get('targetHighPrice'),
    'targetLowPrice': stock.info.get('targetLowPrice'),
    'targetMeanPrice': stock.info.get('targetMeanPrice'),
    'targetMedianPrice': stock.info.get('targetMedianPrice'),

    # Income & Cash Flow Data
    'totalDebt': stock.info.get('totalDebt'),
    'freeCashflow': stock.info.get('freeCashflow'),
    'operatingCashflow': stock.info.get('operatingCashflow'),
    'netIncomeToCommon': stock.info.get('netIncomeToCommon'),
    'totalRevenue': stock.info.get('totalRevenue'),
    'revenuePerShare': stock.info.get('revenuePerShare'),
    'bookValue': stock.info.get('bookValue'),
    'enterpriseValue': stock.info.get('enterpriseValue'),

'profitMargins': stock.info.get('profitMargins'),

    # Other Data
    'currency': stock.info.get('currency'),
    'shortRatio': stock.info.get('shortRatio'),
    'volume': stock.info.get('volume'),
    'regularMarketVolume': stock.info.get('regularMarketVolume'),
    'averageVolume': stock.info.get('averageVolume'),
    'averageVolume10days': stock.info.get('averageVolume10days'),
    'averageDailyVolume10Day': stock.info.get('averageDailyVolume10Day'),
    'overallRisk': stock.info.get('overallRisk'),
    'lastFiscalYearEnd': stock.info.get('lastFiscalYearEnd'),
    'nextFiscalYearEnd': stock.info.get('nextFiscalYearEnd'),
    'mostRecentQuarter': stock.info.get('mostRecentQuarter'),
    'earningsQuarterlyGrowth': stock.info.get('earningsQuarterlyGrowth'),
}

# Print the data in a more organized format
for category, values in data.items():
    print(f'{category}: {values}')
