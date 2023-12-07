from flask import Flask, request, render_template,jsonify
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict_price', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            new_data = {
                'area': float(request.form['area']),
                'bedrooms': int(request.form['bedrooms']),
                'bathrooms': int(request.form['bathrooms']),
                'stories': int(request.form['stories']),
                'mainroad': int(request.form['mainroad']),
                'guestroom': int(request.form['guestroom']),
                'basement': int(request.form['basement']),
                'hotwaterheating': int(request.form['hotwaterheating']),
                'airconditioning': int(request.form['airconditioning']),
                'parking': int(request.form['parking']),
                'prefarea': int(request.form['prefarea']),
                'furnishingstatus_furnished': 1 if request.form['furnishingstatus'] == 'furnished' else 0,
                'furnishingstatus_semi-furnished': 1 if request.form['furnishingstatus'] == 'semi-furnished' else 0,
                'furnishingstatus_unfurnished': 1 if request.form['furnishingstatus'] == 'unfurnished' else 0
                
            }
            new_input_data = pd.DataFrame([new_data])
            loaded_scaler = joblib.load('scaler.joblib')
            lr= joblib.load("LR_model")
            loaded_pca_components = joblib.load('pca_components.joblib')
            new_input_data_normalized = loaded_scaler.transform(new_input_data)
            new_input_data_pca = np.dot(new_input_data_normalized, loaded_pca_components.T)
            predicted_price = lr.predict(new_input_data_pca)
            return jsonify({'predicted_price': float(predicted_price[0])})
        except Exception as e:
            return jsonify({'error': str(e)})        

if __name__ == '__main__':
    app.run(debug=True)
