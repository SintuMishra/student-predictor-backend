import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib

# Load dataset
df = pd.read_csv("data.csv")

# Convert labels
df["result"] = df["result"].map({"Pass": 1, "Fail": 0})

# Features and target
X = df[["hours", "attendance", "previous_marks"]]
y = df["result"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "model.pkl")

print("✅ Model trained and saved as model.pkl")