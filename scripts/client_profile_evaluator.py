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
max_income = 500000  # upper range for high-income clients
min_income = 30000  # entry-level income
max_expenses = 15000  # upper personal expenses
min_expenses = 1000  # minimum personal expenses

# Normalize the factors (scale from 0 to 1 for easier comparison)
age_normalized = (data['Age'] - min_age) / (max_age - min_age)
income_normalized = (data['Income'] - min_income) / (max_income - min_income)
expenses_normalized = (data['Expenses'] - min_expenses) / (max_expenses - min_expenses)
time_horizon_normalized = data['Time_Horizon'] / 30  # assuming 30 years max horizon
risk_tolerance_normalized = data['Risk_Tolerance'] / 5
financial_stability_normalized = data['Financial_Stability'] / 5

# Apply non-linear transformations with more moderate scaling
age_effect = np.sqrt(age_normalized) * 0.5  # adjusted scale
income_effect = np.log(income_normalized + 1) * 0.3  # reduced log impact
expenses_effect = np.sqrt(expenses_normalized) * 0.4  # moderate effect for expenses
time_horizon_effect = np.log(time_horizon_normalized + 1) * 0.5  # mild log instead of exp
risk_tolerance_effect = (risk_tolerance_normalized ** 1.2) * 0.4  # slightly reduced exponent
financial_stability_effect = np.log(financial_stability_normalized + 1) * 0.3  # moderate log effect

# Combine the effects into a simulated MAR score without explicit weightages
MAR_simulated = (age_effect + income_effect + expenses_effect +
                 time_horizon_effect + risk_tolerance_effect + financial_stability_effect)

# Apply an overall scaling factor to limit MAR to a practical range
MAR_percentage = MAR_simulated   # Scaling to bring MAR within a practical range

print(f"Simulated MAR Percentage (with adjustments): {MAR_percentage:.2f}%")
