def risk_assessment_model(ladi_salary, mosun_salary, num_children, cost_of_living_atlanta, age, investment_phase,
                          liquidityPercentage, inflation_rate_atlanta=0.025):
    family_income = ladi_salary + mosun_salary
    childCost = 10000
    yearsToInvestment = investment_phase - 2024

    adjusted_cost_of_living_atlanta = cost_of_living_atlanta * ((1 + inflation_rate_atlanta) ** yearsToInvestment)
    annualCostAtlanta = adjusted_cost_of_living_atlanta * 12  # monthly to annual

    annualExpenses = annualCostAtlanta + (num_children * childCost)

    savings = family_income - annualExpenses

    if savings > 100000 and age < 40:
        risk_tolerance = "High"
    elif 50000 < savings <= 100000:
        risk_tolerance = "Medium"
    else:
        risk_tolerance = "Low"

    availableInvestmentAmount = (savings * (100 - liquidityPercentage)) / 100

    return {
        "Family Income": family_income,
        "Adjusted Annual Expenses (Atlanta)": round(annualExpenses, 2),
        "Savings Potential": round(savings, 2),
        "Risk Tolerance": risk_tolerance,
        "Available Amount": availableInvestmentAmount
    }


ladi_salary = 200000
mosun_salary = 200000
num_children = 2
cost_of_living_atlanta = 6000  # Monthly
age = 32
investment_phase = 2030
liquidityPercentage = 25

result = risk_assessment_model(ladi_salary, mosun_salary, num_children, cost_of_living_atlanta, age, investment_phase)
print("\n--- Risk Assessment Results ---")
print(f"Family Income: ${result['Family Income']}")
print(f"Adjusted Annual Expenses (Atlanta): f${result['Adjusted Annual Expenses (Atlanta)']}")
print(f"Savings Potential: ${result['Savings Potential']}")
print(f"Available amount to invest: ${result['Available Amount']}")
print(f"Risk Tolerance: {result['Risk Tolerance']}")
