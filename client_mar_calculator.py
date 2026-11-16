def risk_assessment_model(ladi_salary, mosun_salary, num_children, cost_of_living_atlanta, age, investment_phase, 
                          inflation_rate_atlanta=0.025, inflation_rate_nigeria=0.035):
    
    family_income = ladi_salary + mosun_salary
    cost_per_child_per_year = 10000 # $10,000 per child (annual)
    years_to_investment = investment_phase - 2024
    
    # Adjust cost of living in Atlanta based on compounded annual inflation rate for each year
    adjusted_cost_of_living_atlanta = cost_of_living_atlanta * ((1 + inflation_rate_atlanta) ** years_to_investment)
    # Annual cost of living in Atlanta
    annual_cost_of_living_atlanta = adjusted_cost_of_living_atlanta * 12   # monthly to annual
    
    # Estimate the cost of living in Nigeria (as a percentage of Atlanta's adjusted cost of living)
    nigeria_cost_of_living_factor = 0.5 # Assuming Nigeria's living cost is ~50% of Atlanta's
    adjusted_cost_of_living_nigeria = adjusted_cost_of_living_atlanta * nigeria_cost_of_living_factor * ((1 + inflation_rate_nigeria) ** years_to_investment)
    
    
    total_expenses_annual = annual_cost_of_living_atlanta + (num_children * cost_per_child_per_year)
    
    savings_potential = family_income - total_expenses_annual
    

    if savings_potential > 100000 and age < 40:
        risk_tolerance = "High"
    elif 50000 < savings_potential <= 100000:
        risk_tolerance = "Medium"
    else:
        risk_tolerance = "Low"
    

    return {
    "Family Income": family_income,
    "Adjusted Annual Expenses (Atlanta)": round(total_expenses_annual,2),
    "Adjusted Cost of Living (Nigeria)": round(adjusted_cost_of_living_nigeria,2),
    "Savings Potential": round(savings_potential,2),
    "Risk Tolerance": risk_tolerance
     }




ladi_salary = 200000
mosun_salary = 200000
num_children = 2
cost_of_living_atlanta = 6000 # Monthly
age = 32
investment_phase = 2030


result = risk_assessment_model(ladi_salary, mosun_salary, num_children, cost_of_living_atlanta, age, investment_phase)
print("\n--- Risk Assessment Results ---")
print(f"Family Income: ${result['Family Income']}")
print(f"Adjusted Annual Expenses (Atlanta): f${result['Adjusted Annual Expenses (Atlanta)']}")
print(f"Adjusted Cost of Living (Nigeria): ${result['Adjusted Cost of Living (Nigeria)']}")
print(f"Savings Potential: ${result['Savings Potential']}")
print(f"Risk Tolerance: {result['Risk Tolerance']}")


