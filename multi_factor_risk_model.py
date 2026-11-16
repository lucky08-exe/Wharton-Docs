import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import yfinance as yf  # For financial data


def calculate_financial_metrics(data):
    """
    Calculate financial performance metrics for the company.
    :param data: A DataFrame with financial data (revenue, profit, equity, debt).
    :return: Dictionary with financial metrics.
    """
    metrics = {}
    metrics['revenue_growth'] = (data['revenue'][-1] - data['revenue'][0]) / data['revenue'][0]
    metrics['profit_margin'] = data['net_profit'] / data['revenue']
    metrics['roe'] = data['net_profit'] / data['equity']
    metrics['debt_to_equity'] = data['debt'] / data['equity']
    return metrics


def calculate_market_metrics(stock_ticker):
    """
    Calculate market performance metrics using historical stock data.
    :param stock_ticker: Stock ticker symbol.
    :return: Dictionary with market metrics.
    """
    stock_data = yf.download(stock_ticker, period='1y', interval='1d')
    metrics = {}
    metrics['price_trend'] = (stock_data['Close'][-1] - stock_data['Close'][0]) / stock_data['Close'][0]
    metrics['volatility'] = stock_data['Close'].pct_change().std()
    return metrics


def calculate_aggregate_risk(financial_metrics, operational_risk, market_risk):
    """
    Calculate aggregate risk based on weighted risk factors.
    :param financial_metrics: Dictionary of financial risk metrics.
    :param operational_risk: Operational risk score (0-1).
    :param market_risk: Market risk score (0-1).
    :return: Aggregate risk score (0-1).
    """
    financial_risk = financial_metrics['debt_to_equity']  # Example proxy for financial risk
    aggregate_risk = 0.4 * financial_risk + 0.3 * operational_risk + 0.3 * market_risk
    return aggregate_risk


def integrate_sentiment_score(aggregate_risk, fred_sentiment):
    """
    Adjust risk and performance based on sentiment score.
    :param aggregate_risk: Aggregate risk score (0-1).
    :param fred_sentiment: FRED sentiment score (0-1).
    :return: Adjusted score (0-5 scale).
    """
    base_score = 5 - (aggregate_risk * 5)
    sentiment_adjusted = base_score + (fred_sentiment - 0.5) * 2  # Sentiment influence
    return max(1, min(5, sentiment_adjusted))


def company_analysis_pipeline(company_data, stock_ticker, operational_risk, market_risk, fred_sentiment):
    """
    Main pipeline to analyze company performance.
    :param company_data: Financial data (revenue, profit, equity, debt).
    :param stock_ticker: Stock ticker symbol.
    :param operational_risk: Operational risk score (0-1).
    :param market_risk: Market risk score (0-1).
    :param fred_sentiment: FRED sentiment score (0-1).
    :return: Final company performance score (1-5).
    """
    # Financial Metrics
    financial_metrics = calculate_financial_metrics(company_data)

    # Market Metrics
    market_metrics = calculate_market_metrics(stock_ticker)

    # Aggregate Risk
    aggregate_risk = calculate_aggregate_risk(financial_metrics, operational_risk, market_risk)

    # Final Score with Sentiment
    final_score = integrate_sentiment_score(aggregate_risk, fred_sentiment)

    # Combine metrics for reporting
    report = {
        "financial_metrics": financial_metrics,
        "market_metrics": market_metrics,
        "aggregate_risk": aggregate_risk,
        "final_score": final_score
    }
    return report


