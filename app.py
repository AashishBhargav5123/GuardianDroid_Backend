from flask import Flask, request, jsonify
import xgboost as xgb
import json
import numpy as np

app = Flask(__name__)  # ✅ Required!

# Load XGBoost Model
model = xgb.Booster()
model.load_model("xgboost_model.json")  # Ensure this path is correct!

# ✅ Print the expected feature names
print("Expected Features:", model.feature_names)

@app.route("/")
def home():
    return "GuardianDroid Backend Running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json  # Get JSON data
        print("Received Data:", data)

        # Load model features
        expected_features = model.feature_names

        # ✅ Fill missing features with default value 0
        feature_values = {feature: data.get(feature, 0) for feature in expected_features}

        # Convert input into numpy array
        feature_array = np.array([list(feature_values.values())])

        # Make prediction using the XGBoost model
        dmatrix = xgb.DMatrix(feature_array, feature_names=expected_features)
        prediction = model.predict(dmatrix)

        # Convert prediction to human-readable result
        result = "Malicious" if prediction[0] > 0.5 else "Benign"
        return jsonify({"prediction": result})
    
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
