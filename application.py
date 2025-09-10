from flask import Flask, request, render_template
import pandas as pd
import pickle
from suitableResponse import ResponseByGemini
from suitableResponse import ResponseByClaude
from suitableResponse import ResponseByGPT

app = Flask(__name__)

# Load the model and preprocessor once
with open("adaboost_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("preprocessor.pkl", "rb") as f:
    preprocessor = pickle.load(f)

with open("label_encoder.pkl", "rb") as f:
    le = pickle.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('index.html')
    
    # Collect inputs from form
    data_dict = {
        "Age": [int(request.form.get('Age'))],
        "Gender": [request.form.get('Gender')],
        "Sleep Quality (1-10)": [int(request.form.get('Sleep Quality (1-10)'))],
        "Stress Level (1-10)": [int(request.form.get('Stress Level (1-10)'))],
        "Symptom Severity (1-10)": [int(request.form.get('Symptom Severity (1-10)'))],
        "Mood Score (1-10)": [int(request.form.get('Mood Score (1-10)'))],
        "Physical Activity (hrs/week)": [int(request.form.get('Physical Activity (hrs/week)'))]
    }

    # Convert to DataFrame
    df = pd.DataFrame(data_dict)

    # Preprocess the input
    df_processed = preprocessor.transform(df)

    # Make prediction
    prediction = model.predict(df_processed)
    
    result=le.inverse_transform(prediction)
    print(prediction)
    
    print(result[0])

    sentence=f"{data_dict} is the person details and it's disease is {result[0]} Tell me possible solutions"

    response=ResponseByGemini(True,'GEMINI_KEY',sentence)

    print(response)
    
    return render_template('index.html', results=result[0],solution=response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
