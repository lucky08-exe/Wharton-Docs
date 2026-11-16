# Circuit Capital: Post-Modern Portfolio Theory & Multi-Asset Allocation Engine
### Wharton Global High School Investment Competition (WGHSIC) 2024–2025

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Strategy-Post--Modern%20Portfolio%20Theory-emerald.svg)]()
[![Optimization](https://img.shields.io/badge/Optimization-Sortino%20Ratio%20%7C%20Downside%20Risk-orange.svg)]()
[![Competition](https://img.shields.io/badge/Competition-Wharton%20WGHSIC%202024--25-purple.svg)](https://globalyouth.wharton.upenn.edu/investment-competition/)

---

## Executive Summary

**Circuit Capital** is a quantitative investment strategy developed for the **Wharton Global High School Investment Competition 2024–2025** by students from **Amity International School, Noida**. 

Rather than relying on classic Modern Portfolio Theory (MPT / Markowitz mean-variance optimization), which penalizes upside volatility equally with downside losses, Circuit Capital employs **Post-Modern Portfolio Theory (PMPT)**. The engine optimizes multi-asset portfolio weights across equities, ETFs, and US Treasury bonds by maximizing the **Sortino Ratio** relative to a dynamic, client-specific **Minimum Acceptable Return (MAR)** threshold ($MAR = 10.06\%$).

```
                      E(R_p) - MAR
  Sortino Ratio = ────────────────────
                  Downside Deviation_p
```

---

## Key Quantitative Pillars

### 1. Client-Side Cash Flow & MAR Engine (`client_mar_calculator.py`)
- Analyzes the client's financial profile (Ladi & Mosun, Atlanta, GA), factoring in family income, Atlanta-specific inflation compounding ($2.5\%$ p.a.), education costs, and dual-country living adjustments.
- Establishes a customized **Minimum Acceptable Return (MAR)** of **10.06%**, setting the benchmark threshold below which volatility is classified as harmful downside risk.

### 2. Multi-Year Risk Projection via Random Forest (`rf_risk_projection.py`)
- Employs a **Random Forest Regressor** to model non-linear interactions among financial stability, compounding expenses, discretionary cash flow, and risk tolerance across a 5-year investment horizon.

### 3. 3-Layer Fundamental & Risk Screening (`financial_ratios_analyzer.py`, `multi_factor_risk_model.py`)
- **Layer 1 (Profitability)**: Filters assets on Return on Equity (ROE), operating margins, and free cash flow generation.
- **Layer 2 (Solvency & Financial Health)**: Screens Current Ratio, Quick Ratio, and Debt-to-Equity thresholds.
- **Layer 3 (Valuation & Market Sensitivity)**: Analyzes forward P/E, PEG ratios, beta, and downside semi-variance. Normalizes metrics using `MinMaxScaler` to produce a composite risk score.

### 4. Macroeconomic Sensitivity Model (`macro_ols_regression.py`)
- Connects to the **Federal Reserve Bank of St. Louis (FRED)** API to evaluate equity and sector sensitivity to CPI inflation, interest rate hikes, and sovereign yield curves via OLS regression.

### 5. Multi-Asset Sortino Optimization Pipeline (`sortino_portfolio_optimizer.py`, `sortino_optimizer_constrained.py`)
- Uses `scipy.optimize.minimize` (SLSQP) to establish optimal portfolio weights across Wharton's approved universe of stocks, ETFs, and US Treasury bonds subject to:
  $$\sum w_i = 1, \quad 0 \le w_i \le w_{\text{max}}$$
  $$\text{Maximize } \text{Sortino}(w) \iff \text{Minimize } -\left(\frac{w^T \mu - \text{MAR}}{\sqrt{\frac{1}{T}\sum \min(0, R_{pt} - \text{MAR})^2}}\right)$$

---

## Repository Structure

```text
├── README.md                          # Project documentation & strategy overview
├── requirements.txt                   # Environment dependencies
├── .gitignore                         # Pre-configured version control ignore rules
│
├── asset_class_sortino_optimizer.py   # Scipy macro asset class optimizer (Stocks vs ETFs vs Bonds)
├── client_mar_calculator.py           # Client inflation-adjusted cash flow & MAR model
├── dataInput.py                       # Market data ingestion & cleaning pipeline
├── exchange_country_mapping.py        # Global exchange-to-sovereign country mapper
├── financial_ratios_analyzer.py       # 3-layer fundamental & solvency ratio screener
├── macro_ols_regression.py            # FRED macroeconomic indicator OLS regression
├── multi_factor_risk_model.py         # Multi-factor aggregate risk scoring model
├── rf_risk_projection.py              # Random Forest multi-year client risk model
├── sortino_optimizer_constrained.py   # Constrained portfolio optimization engine
├── sortino_portfolio_optimizer.py     # Core Sortino ratio portfolio optimizer
│
├── 1) Final Reports/                  # Final competition deliverables & slide decks
│   ├── FINAL WHARTON REPORT -13DEC.docx   # Complete 10-week final submission report
│   ├── CircuitCapital-...MIDTERM.pdf      # Submitted Midterm report
│   ├── Circuit Capital_Asset Allocation.pdf # Asset allocation presentation deck
│   └── CLIENT ANALYSIS + RISK MODEL.pdf   # Client analysis presentation deck
│
├── 2) Research And Strategy/          # Qualitative research & analytical frameworks
│   ├── Analyzing Sortino Ratios...docx    # PMPT & Downside Risk analytical thesis
│   ├── Company Model .docx                # 3-layer company screening methodology
│   ├── mixed approach.docx                # Hybrid top-down vs bottom-up strategy
│   ├── Recommendation & Rebalancing.docx  # Moving average buy/hold/sell signals
│   └── [Country macro profiles]           # Qualitative deep dives (USA, India, China)
│
├── 3) Results/                        # Output portfolio models & scoring matrices
│   ├── final portfolio.xlsx               # Final approved asset weights & selected securities
│   ├── Macrotable.xlsx                    # Sovereign macroeconomic scoring matrix
│   └── Book1.xlsx                         # Performance & returns tracking model
│
├── 4) Output/                         # Processed return matrices & validated asset lists
│   ├── investment_returns.xlsx            # Master daily return matrices across universe
│   ├── stocks_returns.xlsx / etfs_returns.xlsx
│   └── valid/                             # Validated tickers (stocks, ETFs, bonds)
│
├── input/                             # Wharton 2024–2025 approved asset universe
│   ├── FINAL 24-25 Approved Stock List.xlsx
│   ├── FINAL 24-25 Approved ETF List.xlsx
│   └── FINAL 24-25 Approved US Treasury Bonds List.xlsx
│
└── scripts/                           # Auxiliary utilities, downloaders & scratchpads
```

---

## Getting Started

### Prerequisites
- Python 3.10 or higher
- Git

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/wharton-circuit-capital.git
   cd wharton-circuit-capital
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. *(Optional)* Set up FRED API Key for macroeconomic regression:
   ```bash
   # On Windows (PowerShell):
   $env:FRED_API_KEY="your_api_key_here"
   # On macOS/Linux:
   export FRED_API_KEY="your_api_key_here"
   ```

### Running the Models
- **Calculate Client MAR & Risk Profile:**
  ```bash
  python client_mar_calculator.py
  ```
- **Run Fundamental Screening:**
  ```bash
  python financial_ratios_analyzer.py
  ```
- **Execute Sortino Portfolio Optimization:**
  ```bash
  python sortino_portfolio_optimizer.py
  ```

---

## Final Portfolio Composition Highlights

The final allocation balances high-conviction quality compounders with defensive treasury buffers:

| Asset Class | Representative Holdings | Role in Portfolio |
| :--- | :--- | :--- |
| **Equities (Core Compounders)** | `NVDA`, `ASML`, `MSFT`, `GOOGL`, `BLK`, `MA`, `INFY` | Long-term capital appreciation, high ROE, technological moat |
| **Defensive & Dividend Equities** | `ABT`, `FTS`, `PEP`, `HSBA`, `CVX` | Non-cyclical dividend cash flows, low beta |
| **Exchange-Traded Funds (ETFs)** | `VOO`, `VGT`, `IEFA`, `ICLN` | Broad market liquidity, international diversification |
| **US Treasury Bonds** | US T-Bonds (5.00% – 6.625% coupons) | Capital preservation, fixed income hedge against downside volatility |

---

## Authors & Acknowledgements

* **Team:** Circuit Capital
* **School:** Amity International School, Noida, India
* **Competition:** Wharton Global High School Investment Competition (WGHSIC) 2024–2025
* **Host Institution:** Wharton School of the University of Pennsylvania

---

## Disclaimer
*This repository contains academic research and competition submissions prepared for the Wharton Global High School Investment Competition. The models, allocations, and code are for educational and showcase purposes only and do not constitute professional financial advice.*
