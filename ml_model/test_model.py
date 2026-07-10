import pickle

# Load model
model = pickle.load(open("model.pkl", "rb"))

# Test input
hour = 18        # 6 PM
day_type = 1     # weekend

prediction = model.predict([[hour, day_type]])

print("Predicted Crowd:", round(prediction[0]))