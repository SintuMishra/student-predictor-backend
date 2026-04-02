from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib

app = Flask(__name__)

# ✅ Simple and reliable CORS
CORS(app)

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