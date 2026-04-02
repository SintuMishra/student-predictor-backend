from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os

app = Flask(__name__)

# ✅ FIXED CORS
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

model = joblib.load("model.pkl")

@app.route("/")
def home():
    return "API Running"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    prediction = model.predict([[
        data["hours"],
        data["attendance"],
        data["marks"]
    ]])

    result = "Pass" if prediction[0] == 1 else "Fail"

    return jsonify({"result": result})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)