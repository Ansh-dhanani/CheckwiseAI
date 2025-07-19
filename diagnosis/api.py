from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load the model and label encoder
model = joblib.load('cbc_disease_model.joblib')
label_encoder = joblib.load('disease_label_encoder.joblib')

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        
        # Extract features in the correct order
        features = [
            'WBC', 'LY%', 'MO%', 'NE%', 'EO%', 'BA%', 'LY#', 'MO#', 'NE#', 'EO#', 'BA#',
            'RBC', 'HGB', 'HCT', 'MCV', 'MCHC', 'MCH', 'RDW', 'PLT', 'MPV', 'Age', 'Gender'
        ]
        
        # Create input array
        input_data = []
        for feature in features:
            if feature not in data:
                return jsonify({'error': f'Missing feature: {feature}'}), 400
            input_data.append(float(data[feature]))
        
        # Make prediction
        input_array = np.array([input_data])
        prediction_encoded = model.predict(input_array)[0]
        prediction = label_encoder.inverse_transform([prediction_encoded])[0]
        
        # Get prediction probabilities
        probabilities = model.predict_proba(input_array)[0]
        
        # Get top 3 predictions with probabilities
        top_indices = np.argsort(probabilities)[::-1][:3]
        top_predictions = [
            {
                'disease': label_encoder.inverse_transform([idx])[0],
                'probability': float(probabilities[idx])
            }
            for idx in top_indices if probabilities[idx] > 0.01
        ]
        
        return jsonify({
            'prediction': prediction,
            'top_predictions': top_predictions,
            'success': True
        })
        
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/diseases', methods=['GET'])
def get_diseases():
    try:
        diseases = label_encoder.classes_.tolist()
        return jsonify({
            'diseases': diseases,
            'success': True
        })
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)