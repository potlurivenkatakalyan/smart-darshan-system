import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

# Step 1: Load dataset (or create if not exists)
data = pd.DataFrame({
    'hour': [6, 8, 10, 12, 15, 18, 20, 22],
    'day_type': [0, 0, 1, 0, 1, 2, 2, 1],  # 0=weekday,1=weekend,2=festival
    'crowd': [50, 120, 200, 350, 500, 800, 900, 400]
})

# Step 2: Features (X) and Target (y)
X = data[['hour', 'day_type']]
y = data['crowd']

# Step 3: Train model
model = LinearRegression()
model.fit(X, y)

# Step 4: Save model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained & saved successfully!")