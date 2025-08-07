from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
import os
import sys
import logging
import traceback
from datetime import datetime
from file_processor import FileProcessor

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Global variables for model and encoder
model = None
label_encoder = None
model_load_status = {}
current_extracted_data = None

def load_models():
    """Load ML models with proper error handling"""
    global model, label_encoder, model_load_status
    
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_dir, 'cbc_disease_model.joblib')
        encoder_path = os.path.join(current_dir, 'disease_label_encoder.joblib')
        
        logger.info(f"Loading models from: {current_dir}")
        
        if os.path.exists(model_path) and os.path.exists(encoder_path):
            model = joblib.load(model_path)
            label_encoder = joblib.load(encoder_path)
            model_load_status = {'status': 'success', 'message': 'Models loaded successfully'}
            logger.info("Models loaded successfully")
            return True
        else:
            model_load_status = {'status': 'error', 'message': 'Model files not found'}
            logger.error("Model files not found")
            return False
            
    except Exception as e:
        error_msg = f"Error loading models: {str(e)}"
        model_load_status = {'status': 'error', 'message': error_msg}
        logger.error(error_msg)
        return False

@app.route('/api/predict', methods=['POST'])
def predict():
    """Enhanced prediction endpoint with comprehensive validation"""
    if model is None or label_encoder is None:
        if not load_models():
            return jsonify({
                'error': 'Models not available',
                'success': False,
                'model_status': model_load_status
            }), 500
    
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided', 'success': False}), 400
        
        # Extract features in the correct order
        features = [
            'WBC', 'LY%', 'MO%', 'NE%', 'EO%', 'BA%', 'LY#', 'MO#', 'NE#', 'EO#', 'BA#',
            'RBC', 'HGB', 'HCT', 'MCV', 'MCHC', 'MCH', 'RDW', 'PLT', 'MPV', 'Age', 'Gender'
        ]
        
        # Only use defaults for critical missing parameters
        critical_params = ['WBC', 'RBC', 'HGB', 'HCT', 'PLT', 'Age', 'Gender']
        defaults = {
            'WBC': 7.5, 'RBC': 4.8, 'HGB': 14, 'HCT': 42, 'PLT': 250, 'Age': 35, 'Gender': 1
        }
        
        # Create input array with validation
        input_data = []
        missing_params = []
        invalid_params = []
        warnings = []
        
        for feature in features:
            if feature not in data or data[feature] is None or data[feature] == '':
                if feature in critical_params:
                    input_data.append(defaults[feature])
                else:
                    input_data.append(0)
                missing_params.append(feature)
            else:
                try:
                    value = float(data[feature])
                    if validate_parameter_range(feature, value):
                        input_data.append(value)
                    else:
                        input_data.append(value)
                        invalid_params.append(f"{feature}={value}")
                        warnings.append(f"WARNING: {feature}={value} is outside acceptable range - prediction may be inaccurate")
                except (ValueError, TypeError):
                    if feature in critical_params:
                        input_data.append(defaults[feature])
                    else:
                        input_data.append(0)
                    invalid_params.append(f"{feature}={data[feature]}")
        
        # Calculate data completeness
        completeness = ((len(features) - len(missing_params)) / len(features)) * 100
        
        # Make prediction
        input_array = np.array([input_data])
        prediction_encoded = model.predict(input_array)[0]
        prediction = label_encoder.inverse_transform([prediction_encoded])[0]
        
        # Get prediction probabilities
        probabilities = model.predict_proba(input_array)[0]
        
        # Get top predictions with probabilities
        top_indices = np.argsort(probabilities)[::-1][:5]
        top_predictions = []
        
        for idx in top_indices:
            prob = float(probabilities[idx])
            if prob > 0.01:  # Only include predictions with >1% probability
                disease = label_encoder.inverse_transform([idx])[0]
                top_predictions.append({
                    'disease': disease,
                    'probability': prob,
                    'confidence_level': get_confidence_level(prob)
                })
        
        # Generate interpretation note
        interpretation = generate_interpretation_note(missing_params, warnings, completeness)
        
        return jsonify({
            'prediction': prediction,
            'top_predictions': top_predictions,
            'data_quality': {
                'completeness_percentage': round(completeness, 1),
                'missing_parameters': missing_params,
                'invalid_parameters': invalid_params,
                'warnings': warnings,
                'total_parameters': len(features),
                'provided_parameters': len(features) - len(missing_params)
            },
            'interpretation': interpretation,
            'success': True,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        error_msg = f"Prediction error: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        return jsonify({'error': error_msg, 'success': False}), 500

def validate_parameter_range(param, value):
    ranges = {
        'WBC': (0.1, 200.0), 'RBC': (0.5, 15.0), 'HGB': (1.0, 30.0), 'HCT': (5.0, 80.0),
        'MCV': (30.0, 200.0), 'MCH': (10.0, 60.0), 'MCHC': (15.0, 50.0), 'RDW': (5.0, 40.0),
        'PLT': (1.0, 3000.0), 'MPV': (1.0, 30.0), 'LY%': (0.0, 100.0), 'MO%': (0.0, 100.0),
        'NE%': (0.0, 100.0), 'EO%': (0.0, 100.0), 'BA%': (0.0, 100.0), 'LY#': (0.0, 50.0),
        'MO#': (0.0, 20.0), 'NE#': (0.0, 100.0), 'EO#': (0.0, 20.0), 'BA#': (0.0, 10.0),
        'Age': (0.0, 120.0), 'Gender': (0, 1)
    }
    
    if param in ranges:
        min_val, max_val = ranges[param]
        if value < min_val or value > max_val:
            return False
    return True

def get_confidence_level(probability):
    """Convert probability to confidence level description"""
    if probability >= 0.8:
        return "Very High"
    elif probability >= 0.6:
        return "High"
    elif probability >= 0.4:
        return "Moderate"
    elif probability >= 0.2:
        return "Low"
    else:
        return "Very Low"

def generate_interpretation_note(missing_params, warnings, completeness):
    """Generate interpretation note based on data quality"""
    notes = []
    
    if completeness >= 90:
        notes.append("Excellent data completeness - high confidence in results.")
    elif completeness >= 70:
        notes.append("Good data completeness - reliable results.")
    elif completeness >= 50:
        notes.append("Moderate data completeness - results should be interpreted with caution.")
    else:
        notes.append("Limited data available - results have low confidence.")
    
    if missing_params:
        critical_missing = [p for p in missing_params if p in ['WBC', 'RBC', 'HGB', 'HCT', 'PLT']]
        if critical_missing:
            notes.append(f"Missing critical parameters: {', '.join(critical_missing)}.")
    
    if warnings:
        notes.append("Data validation warnings detected - please verify input values.")
    
    return " ".join(notes)

@app.route('/api/diseases', methods=['GET'])
def get_diseases():
    """Get list of diseases the model can predict"""
    if model is None or label_encoder is None:
        if not load_models():
            return jsonify({
                'error': 'Models not available',
                'success': False,
                'model_status': model_load_status
            }), 500
    
    try:
        diseases = label_encoder.classes_.tolist()
        return jsonify({
            'diseases': sorted(diseases),
            'total_diseases': len(diseases),
            'success': True
        })
    except Exception as e:
        logger.error(f"Error getting diseases: {str(e)}")
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Comprehensive health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'models_loaded': model is not None and label_encoder is not None,
        'model_status': model_load_status,
        'version': '2.0.0'
    })

@app.route('/', methods=['GET'])
def index():
    """Root endpoint with API information"""
    return jsonify({
        'message': 'DiagnosisAI API v2.0.0',
        'status': 'running',
        'endpoints': {
            'health': '/api/health',
            'predict': '/api/predict (POST)',
            'diseases': '/api/diseases',
            'upload': '/api/upload (POST)',
            'parameters': '/api/parameters'
        },
        'models_loaded': model is not None and label_encoder is not None
    })

@app.route('/api/parameters', methods=['GET'])
def get_parameters():
    """Get information about required parameters"""
    parameters = {
        'required': [
            'WBC', 'LY%', 'MO%', 'NE%', 'EO%', 'BA%', 'LY#', 'MO#', 'NE#', 'EO#', 'BA#',
            'RBC', 'HGB', 'HCT', 'MCV', 'MCHC', 'MCH', 'RDW', 'PLT', 'MPV', 'Age', 'Gender'
        ],
        'critical': ['WBC', 'RBC', 'HGB', 'HCT', 'PLT', 'Age', 'Gender'],
        'units': {
            'WBC': '10³/μL', 'RBC': '10⁶/μL', 'HGB': 'g/dL', 'HCT': '%',
            'MCV': 'fL', 'MCH': 'pg', 'MCHC': 'g/dL', 'RDW': '%',
            'PLT': '10³/μL', 'MPV': 'fL', 'Age': 'years',
            'LY%': '%', 'MO%': '%', 'NE%': '%', 'EO%': '%', 'BA%': '%',
            'LY#': '10³/μL', 'MO#': '10³/μL', 'NE#': '10³/μL', 'EO#': '10³/μL', 'BA#': '10³/μL'
        }
    }
    return jsonify(parameters)

@app.route('/api/upload', methods=['POST', 'OPTIONS'])
def upload_file():
    """Enhanced file upload and processing endpoint"""
    if request.method == 'OPTIONS':
        return '', 200
    
    # Reset any previous data on new file upload
    global current_extracted_data
    current_extracted_data = None
    
    try:
        # Validate file upload
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded', 'success': False}), 400
        
        file = request.files['file']
        if not file.filename:
            return jsonify({'error': 'No file selected', 'success': False}), 400
        
        logger.info(f"Processing file: {file.filename}")
        
        # Check file size (limit to 10MB)
        file.seek(0, 2)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > 10 * 1024 * 1024:
            return jsonify({'error': 'File too large (max 10MB)', 'success': False}), 400
        
        if file_size == 0:
            return jsonify({'error': 'Empty file', 'success': False}), 400
        
        # Read file content
        file_content = file.read()
        if not file_content:
            return jsonify({'error': 'Failed to read file content', 'success': False}), 400
        
        # Get patient_id if specified
        patient_id = request.form.get('patient_id')
        if patient_id is not None:
            try:
                patient_id = int(patient_id)
            except ValueError:
                return jsonify({'error': 'Invalid patient_id', 'success': False}), 400
        
        # Process the file
        processor = FileProcessor()
        file_extension = file.filename.split('.')[-1].lower() if '.' in file.filename else ''
        
        if not file_extension:
            return jsonify({'error': 'File type could not be determined', 'success': False}), 400
        
        extracted_data = processor.process_file(file_content, file_extension, patient_id)
        
        if isinstance(extracted_data, dict) and 'error' in extracted_data:
            logger.error(f"Processing error: {extracted_data['error']}")
            return jsonify(extracted_data), 400
        
        # Handle multiple patients
        if isinstance(extracted_data, dict) and extracted_data.get('multiple_patients'):
            return jsonify({
                **extracted_data,
                'success': True
            })
        
        # Clean and validate extracted data
        cleaned_data = {}
        for key, value in extracted_data.items():
            if key.startswith('_'):  # Skip metadata
                continue
            if value is not None and str(value).strip() != '':
                cleaned_data[key] = value
        
        logger.info(f"Successfully extracted {len(cleaned_data)} parameters")
        
        return jsonify({
            'extracted_data': cleaned_data,
            'success': True,
            'message': f'Successfully extracted {len(cleaned_data)} parameters from {file.filename}',
            'file_type': file_extension,
            'file_size': file_size,
            'processing_timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        error_msg = f"Upload processing error: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        return jsonify({'error': error_msg, 'success': False}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found', 'success': False}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error', 'success': False}), 500

if __name__ == '__main__':
    # Try to load models at startup
    logger.info("Starting DiagnosisAI API...")
    load_models()
    
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting server on port {port}, debug={debug_mode}")
    app.run(host='0.0.0.0', debug=debug_mode, port=port)