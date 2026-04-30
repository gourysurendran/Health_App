from flask import Flask, request, render_template
import pickle

app = Flask(__name__)

# Load model
model = pickle.load(open("model.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        age_val = request.form.get("age")
        bmi_val = request.form.get("bmi")
        bp_val = request.form.get("bp")
        
        if not age_val or not bmi_val or not bp_val:
            return render_template("index.html", prediction_text="Error: Please fill all fields.")
            
        age = int(age_val)
        bmi = float(bmi_val)
        bp = int(bp_val)
        
        import pandas as pd
        features = pd.DataFrame([[age, bmi, bp]], columns=['Age', 'BMI', 'BP'])
        prediction = model.predict(features)

        result = ["Low Risk", "Medium Risk", "High Risk"][prediction[0]]
        return render_template("index.html", prediction_text=result, age=age_val, bmi=bmi_val, bp=bp_val)
    except Exception as e:
        return render_template("index.html", prediction_text=f"Error: {str(e)}", age=request.form.get("age", ""), bmi=request.form.get("bmi", ""), bp=request.form.get("bp", ""))

if __name__ == "__main__":
    app.run(debug=True)