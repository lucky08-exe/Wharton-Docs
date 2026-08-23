import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

data = {
    'Age': [],
    'Income': [],
    'Expenses': [],
    'Time_Horizon': [],
    'Risk_Tolerance': [],
    'Financial_Stability': [],
    'Family_Focus': [],
    'MAR': []
}

df = pd.DataFrame(data)

X = df.drop(columns=['MAR'])
y = df['MAR']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor()
model.fit(X_train, y_train)

timeCalc = 5

future_client = pd.DataFrame({
    'Age': [32 + timeCalc],  # Age in timeCalc years
    'Income': [round(200000 * (1 + 0.04) ** timeCalc, 2)],  # Income growth at 4% annually
    'Expenses': [round(6000 * (1 + 0.03) ** timeCalc, 2)],  # Expenses with 3% inflation
    'Time_Horizon': [10 - timeCalc if 10 - timeCalc > 0 else 1],  # Adjusted time horizon
    'Risk_Tolerance': [round(4 - (0.1 * timeCalc), 2) if (4 - 0.1 * timeCalc) > 1 else 1],  # Adjusted risk tolerance
    'Financial_Stability': [round(4 + (0.1 * timeCalc), 2) if (4 + 0.1 * timeCalc) <= 5 else 5],  # Adjusted stability
    'Family_Focus': [round(3 + (0.1 * timeCalc), 2) if (3 + 0.1 * timeCalc) <= 5 else 5]  # Adjusted family focus
})

predicted_mar = model.predict(future_client)
print(f"Predicted MAR for the future client: {predicted_mar[0]}%")
