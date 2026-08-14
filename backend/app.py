
import io
import joblib
import pandas as pd
from flask import Flask, jsonify, request

app = Flask(__name__) # Using 'app' for consistency with common gunicorn usage

# Load the comprehensive scikit-learn processing & prediction pipeline
# Model is copied to /app in Dockerfile, so relative path is fine.
model_pipeline = joblib.load("superkart_model.joblib")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/v1/predict", methods=["POST"]) # Endpoint for online (single) inference
def predict_single():
    """Executes single payload inference requests."""
    try:
        data = request.get_json()
        input_dt = pd.DataFrame([data])

        # Enforce engineered age feature logic inside pipeline mapping
        if "Store_Establishment_Year" in input_dt.columns:
            input_dt["Store_Age"] = 2026 - input_dt["Store_Establishment_Year"]

        prediction = model_pipeline.predict(input_dt)[0]
        return jsonify({"predicted_sales": float(prediction)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/v1/predictbatch", methods=["POST"]) # Endpoint for batch inference
def predict_batch():
    """Executes bulk CSV document batch inference."""
    try:
        file = request.files["file"]
        if not file:
            return jsonify({"error": "No file uploaded"}), 400

        # Read CSV data stream into memory memory frame
        input_dt = pd.read_csv(io.StringIO(file.stream.read().decode("utf-8")))

        if "Store_Establishment_Year" in input_dt.columns:
            input_dt["Store_Age"] = 2026 - input_dt["Store_Establishment_Year"]

        predictions = model_pipeline.predict(input_dt)
        input_dt["Predicted_Product_Store_Sales_Total"] = predictions

        # Return as JSON records
        return input_dt.to_json(orient="records"), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7860) # For local testing within container
