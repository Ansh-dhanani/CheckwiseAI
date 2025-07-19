from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
import os
import sys

app = Flask(__name__)
CORS(app)

# Global variables for model and encoder
model = None
label_encoder = None

def load_models():
    """Load ML models with proper error handling"""
    global model, label_encoder
    
    try:
        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Define model paths
        model_path = os.path.join(current_dir, 'cbc_disease_model.joblib')
        encoder_path = os.path.join(current_dir, 'disease_label_encoder.joblib')
        
        # Print diagnostic info
        print(f"Current directory: {current_dir}")
        print(f"Model path: {model_path}")
        print(f"Encoder path: {encoder_path}")
        print(f"Files exist: Model: {os.path.exists(model_path)}, Encoder: {os.path.exists(encoder_path)}")
        
        # Load models
        if os.path.exists(model_path) and os.path.exists(encoder_path):
            model = joblib.load(model_path)
            label_encoder = joblib.load(encoder_path)
            print("Models loaded successfully")
            return True
        else:
            print("Model files not found")
            return False
            
    except Exception as e:
        print(f"Error loading models: {str(e)}")
        return False

@app.route('/api/predict', methods=['POST'])
def predict():
    # Load models if not already loaded
    if model is None or label_encoder is None:
        if not load_models():
            return jsonify({'error': 'Failed to load models', 'success': False}), 500
    
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
    # Load models if not already loaded
    if model is None or label_encoder is None:
        if not load_models():
            return jsonify({'error': 'Failed to load models', 'success': False}), 500
    
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
    """Health check endpoint that doesn't require models to be loaded"""
    return jsonify({
        'status': 'healthy',
        'models_loaded': model is not None and label_encoder is not None
    })

@app.route('/', methods=['GET'])
def index():
    """Root endpoint for basic verification"""
    return jsonify({
        'message': 'DiagnosisAI API is running',
        'endpoints': ['/api/health', '/api/predict', '/api/diseases']
    })

if __name__ == '__main__':
    # Try to load models at startup
    load_models()
    app.run(debug=True, port=5000)