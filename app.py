from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os

app = Flask(__name__)

# ✅ Proper CORS setup (handles preflight + all origins)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Load ML model
model = joblib.load("model.pkl")

# Home route
@app.route("/")
def home():
    return "API Running"

# Prediction route (IMPORTANT: includes OPTIONS)
@app.route("/predict", methods=["POST", "OPTIONS"])
def predict():
    # ✅ Handle preflight request
    if request.method == "OPTIONS":
        response = jsonify({"message": "Preflight OK"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response, 200

    # Get JSON data
    data = request.get_json()

    # Validate input
    if not data:
        return jsonify({"error": "No input data"}), 400

    hours = data.get("hours")
    attendance = data.get("attendance")
    marks = data.get("marks")

    # Check missing fields
    if hours is None or attendance is None or marks is None:
        return jsonify({"error": "Missing fields"}), 400

    # Prediction
    prediction = model.predict([[hours, attendance, marks]])
    result = "Pass" if prediction[0] == 1 else "Fail"

    # Response
    response = jsonify({"result": result})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

# Run app (Render compatible)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)