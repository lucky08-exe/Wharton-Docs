import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Example: Mean returns for each asset (annualized)
mean_returns = np.array([0.16, 0.105, 0.08])  # Stocks (16%), ETFs (10.5%), Bonds (8%)

# Example: Downside deviations for each asset (annualized)
downside_deviations = np.array([0.04, 0.02, 0.00])  # 4%, 2%, 0%

# Minimum Acceptable Return (MAR) - 10%
mar = 0.10

# Maximum Acceptable Risk (downside deviation) - 90%
max_risk = 0.9

# Objective function: Maximize the Sortino ratio
def sortino_ratio(weights, mean_returns, mar, downside_deviations):
    portfolio_return = np.dot(weights, mean_returns)
    downside_deviation = np.sqrt(np.sum((weights * downside_deviations) ** 2))
    return -(portfolio_return - mar) / downside_deviation  # Negative for minimization

# Constraint to ensure the sum of weights is 1
def weight_constraint(weights):
    return np.sum(weights) - 1

# Constraint to ensure the portfolio downside deviation (risk) <= max acceptable risk
def risk_constraint(weights):
    downside_deviation = np.sqrt(np.sum((weights * downside_deviations) ** 2))
    return max_risk - downside_deviation

# Constraints dictionary
constraints = [
    {'type': 'eq', 'fun': weight_constraint},
    {'type': 'ineq', 'fun': risk_constraint}
]

# Bounds to ensure each asset has at least 5% allocation
bounds = [(0.05, None) for _ in range(len(mean_returns))]  # Minimum 5% allocation

# Optimize portfolio with minimum constraints
result = minimize(sortino_ratio, np.random.random(3),  # Start with random weights
                  args=(mean_returns, mar, downside_deviations),
                  method='SLSQP', constraints=constraints, bounds=bounds)

# Extract optimal portfolio weights
optimal_weights = result.x

# Display results
print(f"Optimal Portfolio Weights: Stocks = {optimal_weights[0]*100:.2f}%, ETFs = {optimal_weights[1]*100:.2f}%, Bonds = {optimal_weights[2]*100:.2f}%")

# Portfolio metrics
optimal_return = np.dot(optimal_weights, mean_returns)
optimal_downside_deviation = np.sqrt(np.sum((optimal_weights * downside_deviations) ** 2))
optimal_sortino_ratio = (optimal_return - mar) / optimal_downside_deviation

print(f"Optimal Portfolio Expected Return: {optimal_return*100:.2f}%")
print(f"Optimal Portfolio Downside Deviation: {optimal_downside_deviation*100:.2f}%")
print(f"Optimal Portfolio Sortino Ratio: {optimal_sortino_ratio:.2f}")

# Efficient Frontier Plot
num_portfolios = 10000
all_weights = np.zeros((num_portfolios, 3))
portfolio_returns = np.zeros(num_portfolios)
portfolio_sortino_ratios = np.zeros(num_portfolios)

for i in range(num_portfolios):
    weights = np.random.random(3)
    weights /= np.sum(weights)  # Normalize weights to sum to 1
    all_weights[i, :] = weights
    portfolio_returns[i] = np.dot(weights, mean_returns)
    portfolio_sortino_ratios[i] = (portfolio_returns[i] - mar) / np.sqrt(np.sum((weights * downside_deviations) ** 2))

plt.scatter(np.sqrt(np.sum((all_weights * downside_deviations) ** 2, axis=1)), portfolio_returns, c=portfolio_sortino_ratios, cmap='viridis', marker='o')
plt.colorbar(label='Sortino Ratio')
plt.title('Efficient Frontier with Sortino Ratio')
plt.xlabel('Risk (Downside Deviation)')
plt.ylabel('Return')
plt.scatter(optimal_downside_deviation, optimal_return, color='red', marker='*', s=200, label="Optimal Portfolio")
plt.legend(loc='best')
plt.show()
