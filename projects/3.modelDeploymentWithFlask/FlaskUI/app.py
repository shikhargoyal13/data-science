# app_ui.py
from flask import Flask, render_template, request
import pickle
import numpy as np

# Load model
with open("iris_model.pkl", "rb") as f:
    model = pickle.load(f)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    if request.method == "POST":
        try:
            features = [
                float(request.form["sepal_length"]),
                float(request.form["sepal_width"]),
                float(request.form["petal_length"]),
                float(request.form["petal_width"])
            ]
            pred = model.predict([np.array(features)])
            prediction = ["setosa", "versicolor", "virginica"][pred[0]]
        except:
            prediction = "Invalid input"

    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
