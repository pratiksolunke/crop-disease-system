from flask import Flask, request, jsonify
from model_logic import load_data, predict_stage_and_disease
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow Streamlit to access API
df = load_data()

@app.route("/")
def home():
    return jsonify({"message": "Crop Disease Predictor API is running!"})

@app.route("/crops", methods=["GET"])
def get_crops():
    crops = sorted(df["crop_name"].str.lower().unique().tolist())
    return jsonify({"crops": crops})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    crop_name = data.get("crop_name")
    sowing_date = data.get("sowing_date")

    if not crop_name or not sowing_date:
        return jsonify({"error": "Missing crop_name or sowing_date"}), 400

    result = predict_stage_and_disease(crop_name, sowing_date, df)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
