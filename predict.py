import joblib

# Load saved model
model = joblib.load("model.pkl")

# User input
hours = float(input("Enter study hours: "))
attendance = float(input("Enter attendance: "))
marks = float(input("Enter previous marks: "))

# Prediction
prediction = model.predict([[hours, attendance, marks]])

if prediction[0] == 1:
    print("Predicted Result: Pass")
else:
    print("Predicted Result: Fail")