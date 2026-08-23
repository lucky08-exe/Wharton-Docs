# ALL CONTENTS OF THIS FILE ARE AI GENERATED


import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

years = 20
time = 5  # Predict for this many years from now

data = {
    'Age': [32 + i for i in range(years)],
    'Income': [round(200000 * (1 + 0.04) ** i, 2) for i in range(years)],
    'Expenses': [round(6000 * (1 + 0.03) ** i, 2) for i in range(years)],
    'Time_Horizon': [10 - i if 10 - i > 0 else 1 for i in range(years)],
    'Family_Focus': [round(3 + 0.1 * i, 2) if (3 + 0.1 * i) <= 5 else 5 for i in range(years)],
}

df = pd.DataFrame(data)

scaler = MinMaxScaler()
normalized_data = scaler.fit_transform(df[['Age', 'Income', 'Expenses', 'Time_Horizon', 'Family_Focus']])
df_normalized = pd.DataFrame(normalized_data, columns=['Age', 'Income', 'Expenses', 'Time_Horizon', 'Family_Focus'])

# Formula for MAR calculation
df['MAR'] = (
    (1 - df_normalized['Age'])  # Age negatively affects
    + df_normalized['Income']  # Income positively affects
    - df_normalized['Expenses']  # Expenses negatively affect
    + df_normalized['Time_Horizon']  # Time horizon positively affects
    - df_normalized['Family_Focus']  # Family focus negatively affects
)


df['MAR'] = df['MAR'] * 10  # scaling to produce values in % terms
df['MAR'] = df['MAR'].clip(lower=0, upper=20)

X = df[['Age', 'Income', 'Expenses', 'Time_Horizon', 'Family_Focus']]
y = df['MAR']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

future_profile = {
    'Age': 32 + time,  # Age in 5 years
    'Income': round(200000 * (1 + 0.04) ** time, 2),  # Income after 5 years
    'Expenses': round(6000 * (1 + 0.03) ** time, 2),  # Expenses after 5 years
    'Time_Horizon': 10 - time if 10 - time > 0 else 1,  # Time horizon decreases with age
    'Family_Focus': round(3 + 0.1 * time, 2) if (3 + 0.1 * time) <= 5 else 5,  # Family focus increases with time
}

future_profile_normalized = scaler.transform(pd.DataFrame([future_profile]))

predicted_mar = model.predict(future_profile_normalized)
print(f"Predicted MAR at Year {time}: {predicted_mar[0]:.2f}%")
