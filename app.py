from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app)  # ✅ allow React to connect

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
    app.run(host="0.0.0.0", port=10000)