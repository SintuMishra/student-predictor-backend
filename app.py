from flask import Flask, request, jsonify
import joblib
import os

app = Flask(__name__)

model = joblib.load("model.pkl")

# ✅ FORCE CORS HEADERS (IMPORTANT)
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    return response


@app.route("/")
def home():
    return "API Running"


@app.route("/predict", methods=["POST", "OPTIONS"])
def predict():
    # ✅ Handle preflight manually
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200

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