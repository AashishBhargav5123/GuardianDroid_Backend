from flask import Flask, request, jsonify
import xgboost as xgb
import json
import numpy as np

app = Flask(__name__)  # ✅ Required!

# Load XGBoost Model
model = xgb.Booster()
model.load_model("xgboost_model.json")  # Ensure this path is correct!

@app.route("/")
def home():
    return "GuardianDroid Backend Running!"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        features = np.array([list(data.values())])
        dmatrix = xgb.DMatrix(features)
        prediction = model.predict(dmatrix)
        result = "Malicious" if prediction[0] > 0.5 else "Benign"
        return jsonify({"prediction": result})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
