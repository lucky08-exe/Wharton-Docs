import numpy as np

# Client data
data = {
    'Age': 32,
    'Income': 200000,
    'Expenses': 6000,
    'Risk_Tolerance': 4,  # on a scale of 1-5
    'Time_Horizon': 5,  # years
    'Financial_Stability': 4,  # on a scale of 1-5
}

# Assumed ranges for normalization
max_age = 60  # average working life (retirement age)
min_age = 22  # typical start of professional life
max_income = 500000  # upper range for high income clients
min_income = 30000  # entry-level income
max_expenses = 15000  # upper personal expenses
min_expenses = 1000  # minimum personal expenses

# Normalize the factors (scale from 0 to 1 for easier comparison)
age_normalized = (data['Age'] - min_age) / (max_age - min_age)  # Normalize age between 0 and 1
income_normalized = (data['Income'] - min_income) / (max_income - min_income)  # Normalize income
expenses_normalized = (data['Expenses'] - min_expenses) / (max_expenses - min_expenses)  # Normalize expenses
time_horizon_normalized = data['Time_Horizon'] / 30  # Normalize time horizon (assuming 30 years max horizon)
risk_tolerance_normalized = data['Risk_Tolerance'] / 5  # Normalize risk tolerance
financial_stability_normalized = data['Financial_Stability'] / 5  # Normalize financial stability

# Apply linear effects for each factor
age_effect = age_normalized  # Linear effect for age
income_effect = income_normalized  # Linear effect for income
expenses_effect = expenses_normalized  # Linear effect for expenses
time_horizon_effect = time_horizon_normalized  # Linear effect for time horizon
risk_tolerance_effect = risk_tolerance_normalized  # Linear effect for risk tolerance
financial_stability_effect = financial_stability_normalized  # Linear effect for financial stability

# Combine the effects into a simulated MAR score
MAR_simulated = (age_effect + income_effect + expenses_effect +
                 time_horizon_effect + risk_tolerance_effect + financial_stability_effect)

# The MAR percentage without clipping
MAR_percentage = MAR_simulated  # Convert the score to percentage

print(f"Simulated MAR Percentage (without clipping): {MAR_percentage:.2f}%")
