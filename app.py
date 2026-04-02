from flask import Flask, request, jsonify
import joblib
import os

app = Flask(__name__)

# Load model
model = joblib.load("model.pkl")

# ✅ Force CORS headers (robust solution)
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


@app.route("/")
def home():
    return "API Running"


@app.route("/predict", methods=["POST", "OPTIONS"])
def predict():
    # ✅ Handle preflight request
    if request.method == "OPTIONS":
        return jsonify({"message": "Preflight OK"}), 200

    try:
        data = request.get_json()

        # Validate input
        if not data:
            return jsonify({"error": "No data provided"}), 400

        hours = data.get("hours")
        attendance = data.get("attendance")
        marks = data.get("marks")

        if hours is None or attendance is None or marks is None:
            return jsonify({"error": "Missing input fields"}), 400

        # Prediction
        prediction = model.predict([[hours, attendance, marks]])
        result = "Pass" if prediction[0] == 1 else "Fail"

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)