import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Define the number of years for projection
years = 5

# Example data for the client's projected values over the next years years
data = {
    'Age': [32 + i for i in range(years)],
    'Income': [round(200000 * (1 + 0.04) ** i, 2) for i in range(years)],
    'Expenses': [round(6000 * (1 + 0.03) ** i, 2) for i in range(years)],
    'Time_Horizon': [10 - i if 10 - i > 0 else 1 for i in range(years)],
    'Risk_Tolerance': [round(4 - 0.1 * i, 2) if (4 - 0.1 * i) > 1 else 1 for i in range(years)],
    'Financial_Stability': [round(4 + 0.1 * i, 2) if (4 + 0.1 * i) <= 5 else 5 for i in range(years)],
    'Family_Focus': [round(3 + 0.1 * i, 2) if (3 + 0.1 * i) <= 5 else 5 for i in range(years)],
    'MAR': [10, 12, 8, 9, 11]  # Example MAR values
}

# Convert the data into a DataFrame
df = pd.DataFrame(data)

# Define features and target
X = df.drop(columns=['MAR'])
y = df['MAR']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest model
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Define future time interval for predictions
timeCalc = 5

# Predict MAR for a future client profile
future_client = pd.DataFrame({
    'Age': [32 + timeCalc],  # Age in timeCalc years
    'Income': [round(200000 * (1 + 0.04) ** timeCalc, 2)],  # Income growth at 4% annually
    'Expenses': [round(6000 * (1 + 0.03) ** timeCalc, 2)],  # Expenses with 3% inflation
    'Time_Horizon': [10 - timeCalc if 10 - timeCalc > 0 else 1],  # Adjusted time horizon
    'Risk_Tolerance': [round(4 - (0.1 * timeCalc), 2) if (4 - 0.1 * timeCalc) > 1 else 1],  # Adjusted risk tolerance
    'Financial_Stability': [round(4 + (0.1 * timeCalc), 2) if (4 + 0.1 * timeCalc) <= 5 else 5],  # Adjusted stability
    'Family_Focus': [round(3 + (0.1 * timeCalc), 2) if (3 + 0.1 * timeCalc) <= 5 else 5]  # Adjusted family focus
})

# Predict the MAR for the future client
predicted_mar = model.predict(future_client)
print(f"Predicted MAR for the future client: {predicted_mar[0]}%")