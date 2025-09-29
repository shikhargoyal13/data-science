# app_api.py
from flask import Flask, request, jsonify
import pickle
import numpy as np

# Load model
with open("iris_model.pkl", "rb") as f:
    model = pickle.load(f)

app = Flask(__name__)

@app.route("/")
def home():
    return {"message": "Iris Prediction API is running!"}

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()  # Expect JSON
    features = data.get("features")  # e.g. [5.1, 3.5, 1.4, 0.2]

    if not features or len(features) != 4:
        return jsonify({"error": "Provide 4 features: sepal_length, sepal_width, petal_length, petal_width"}), 400

    prediction = model.predict([np.array(features)])
    species = ["setosa", "versicolor", "virginica"][prediction[0]]

    return jsonify({"prediction": species})

if __name__ == "__main__":
    app.run(debug=True)

