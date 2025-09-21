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

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Global variables for model and encoder
model = None
label_encoder = None
model_load_status = {}

# Unit conversion functions
def convert_to_default_unit(parameter, value, from_unit):
    """Convert parameter value from given unit to default unit"""
    conversion_factors = {
        'HGB': {
            'g/L': 0.1,  # g/L to g/dL
            'mmol/L': 1.61  # mmol/L to g/dL (approximate)
        },
        'MCHC': {
            'g/L': 0.1,  # g/L to g/dL
            'mmol/L': 1.61  # mmol/L to g/dL (approximate)
        },
        'WBC': {
            'K/μL': 1.0,  # K/μL is same as 10³/μL
            'cells/μL': 0.001,  # cells/μL to 10³/μL
            '10⁹/L': 1.0  # 10⁹/L is same as 10³/μL
        },
        'RBC': {
            'M/μL': 1.0,  # M/μL is same as 10⁶/μL
            'cells/μL': 0.000001,  # cells/μL to 10⁶/μL
            '10¹²/L': 1.0  # 10¹²/L is same as 10⁶/μL
        },
        'PLT': {
            'K/μL': 1.0,  # K/μL is same as 10³/μL
            'cells/μL': 0.001,  # cells/μL to 10³/μL
            '10⁹/L': 1.0  # 10⁹/L is same as 10³/μL
        },
        'LY#': {
            'K/μL': 1.0,
            'cells/μL': 0.001,
            '10⁹/L': 1.0
        },
        'MO#': {
            'K/μL': 1.0,
            'cells/μL': 0.001,
            '10⁹/L': 1.0
        },
        'NE#': {
            'K/μL': 1.0,
            'cells/μL': 0.001,
            '10⁹/L': 1.0
        },
        'EO#': {
            'K/μL': 1.0,
            'cells/μL': 0.001,
            '10⁹/L': 1.0
        },
        'BA#': {
            'K/μL': 1.0,
            'cells/μL': 0.001,
            '10⁹/L': 1.0
        },
        'HCT': {
            'L/L': 100.0,  # L/L to %
            'fraction': 100.0  # fraction to %
        },
        'Age': {
            'months': 1/12,  # months to years
            'days': 1/365.25  # days to years
        },
        # Percentage conversions
        'LY%': {'fraction': 100.0},
        'MO%': {'fraction': 100.0},
        'NE%': {'fraction': 100.0},
        'EO%': {'fraction': 100.0},
        'BA%': {'fraction': 100.0}
    }
    
    if parameter in conversion_factors and from_unit in conversion_factors[parameter]:
        return value * conversion_factors[parameter][from_unit]
    return value

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
    """Enhanced prediction endpoint with comprehensive validation and improved error handling"""
    if model is None or label_encoder is None:
        if not load_models():
            return jsonify({
                'error': 'ML models not available. Please check server configuration.',
                'success': False,
                'model_status': model_load_status
            }), 500
    
    try:
        data = request.json
        if not data:
            return jsonify({
                'error': 'No data provided. Please send CBC parameters in JSON format.',
                'success': False
            }), 400
        
        # Validate and process input data
        validation_result = validate_and_process_input(data)
        if validation_result.get('error'):
            return jsonify(validation_result), 400
        
        input_data = validation_result['input_data']
        data_quality = validation_result['data_quality']
        
        # Make prediction with error handling
        try:
            input_array = np.array([input_data])
            prediction_encoded = model.predict(input_array)[0]
            prediction = label_encoder.inverse_transform([prediction_encoded])[0]
            
            # Get prediction probabilities
            probabilities = model.predict_proba(input_array)[0]
            
            # Get top predictions with probabilities
            top_predictions = get_top_predictions(probabilities, label_encoder, min_probability=0.01)
            
            # Generate comprehensive analysis
            analysis = generate_comprehensive_analysis(data_quality, top_predictions[0]['probability'] if top_predictions else 0)
            
            return jsonify({
                'prediction': prediction,
                'top_predictions': top_predictions,
                'data_quality': data_quality,
                'analysis': analysis,
                'success': True,
                'timestamp': datetime.now().isoformat(),
                'model_version': '2.1.0'
            })
            
        except Exception as pred_error:
            logger.error(f"Model prediction failed: {str(pred_error)}")
            return jsonify({
                'error': 'Prediction model encountered an error. Please check your input data.',
                'success': False
            }), 500
        
    except Exception as e:
        error_msg = f"Prediction endpoint error: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        return jsonify({
            'error': 'Internal server error occurred during prediction.',
            'success': False
        }), 500

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

def validate_and_process_input(data):
    """Validate and process input data with enhanced error handling"""
    features = [
        'WBC', 'LY%', 'MO%', 'NE%', 'EO%', 'BA%', 'LY#', 'MO#', 'NE#', 'EO#', 'BA#',
        'RBC', 'HGB', 'HCT', 'MCV', 'MCHC', 'MCH', 'RDW', 'PLT', 'MPV', 'Age', 'Gender'
    ]
    
    critical_params = ['WBC', 'RBC', 'HGB', 'HCT', 'PLT', 'Age', 'Gender']
    defaults = {
        'WBC': 7.5, 'RBC': 4.8, 'HGB': 14, 'HCT': 42, 'PLT': 250, 'Age': 35, 'Gender': 1
    }
    
    input_data = []
    missing_params = []
    invalid_params = []
    warnings = []
    out_of_range_params = []
    
    for feature in features:
        if feature not in data or data[feature] is None or data[feature] == '':
            if feature in critical_params:
                input_data.append(defaults[feature])
                missing_params.append(feature)
            else:
                input_data.append(0)  # Use 0 for non-critical missing parameters
                missing_params.append(feature)
        else:
            try:
                value = float(data[feature])
                
                # Validate range
                if not validate_parameter_range(feature, value):
                    out_of_range_params.append(f"{feature}={value}")
                    warnings.append(f"WARNING: {feature}={value} is outside normal range")
                
                input_data.append(value)
                
            except (ValueError, TypeError):
                if feature in critical_params:
                    input_data.append(defaults[feature])
                    missing_params.append(feature)
                else:
                    input_data.append(0)
                    missing_params.append(feature)
                invalid_params.append(f"{feature}={data[feature]}")
    
    # Calculate data quality metrics
    completeness = ((len(features) - len(missing_params)) / len(features)) * 100
    
    # Check if we have enough data to make a reliable prediction
    critical_missing = [p for p in missing_params if p in critical_params]
    if len(critical_missing) > 3:  # Too many critical parameters missing
        return {
            'error': f'Too many critical parameters missing: {", ".join(critical_missing)}. Please provide at least basic CBC values.',
            'success': False
        }
    
    data_quality = {
        'completeness_percentage': round(completeness, 1),
        'missing_parameters': missing_params,
        'invalid_parameters': invalid_params,
        'out_of_range_parameters': out_of_range_params,
        'warnings': warnings,
        'total_parameters': len(features),
        'provided_parameters': len(features) - len(missing_params),
        'critical_missing': critical_missing
    }
    
    return {
        'input_data': input_data,
        'data_quality': data_quality,
        'success': True
    }

def get_top_predictions(probabilities, label_encoder, min_probability=0.01, max_predictions=5):
    """Get top predictions with probabilities"""
    top_indices = np.argsort(probabilities)[::-1][:max_predictions]
    top_predictions = []
    
    for idx in top_indices:
        prob = float(probabilities[idx])
        if prob >= min_probability:
            disease = label_encoder.inverse_transform([idx])[0]
            top_predictions.append({
                'disease': disease,
                'probability': prob,
                'percentage': round(prob * 100, 2),
                'confidence_level': get_confidence_level(prob)
            })
    
    return top_predictions

def generate_comprehensive_analysis(data_quality, primary_confidence):
    """Generate comprehensive analysis based on data quality and prediction confidence"""
    analysis = {
        'reliability': 'Unknown',
        'recommendation': '',
        'notes': []
    }
    
    # Assess reliability
    completeness = data_quality['completeness_percentage']
    critical_missing = len(data_quality['critical_missing'])
    warnings = len(data_quality['warnings'])
    
    if completeness >= 95 and critical_missing == 0 and warnings == 0:
        analysis['reliability'] = 'Excellent'
        analysis['recommendation'] = 'High confidence prediction. Results are reliable for clinical reference.'
    elif completeness >= 80 and critical_missing <= 1 and warnings <= 2:
        analysis['reliability'] = 'Good'
        analysis['recommendation'] = 'Good quality prediction. Minor data gaps present but results are trustworthy.'
    elif completeness >= 60 and critical_missing <= 2:
        analysis['reliability'] = 'Fair'
        analysis['recommendation'] = 'Fair prediction quality. Some important parameters missing. Use with caution.'
    else:
        analysis['reliability'] = 'Poor'
        analysis['recommendation'] = 'Low confidence prediction. Too many missing or invalid parameters. Obtain complete CBC results.'
    
    # Add specific notes
    if critical_missing > 0:
        analysis['notes'].append(f"Missing {critical_missing} critical parameter(s)")
    
    if warnings > 0:
        analysis['notes'].append(f"{warnings} parameter(s) outside normal range")
    
    if primary_confidence < 0.3:
        analysis['notes'].append("Low prediction confidence - multiple conditions possible")
    elif primary_confidence > 0.8:
        analysis['notes'].append("High prediction confidence")
    
    return analysis

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
    """Comprehensive health check endpoint with detailed system information"""
    models_loaded = model is not None and label_encoder is not None
    
    health_data = {
        'status': 'healthy' if models_loaded else 'degraded',
        'timestamp': datetime.now().isoformat(),
        'version': '2.1.0',
        'models': {
            'disease_model_loaded': model is not None,
            'label_encoder_loaded': label_encoder is not None,
            'total_diseases': len(label_encoder.classes_) if label_encoder is not None else 0,
            'model_status': model_load_status
        },
        'system': {
            'python_version': sys.version.split()[0],
            'flask_running': True,
            'cors_enabled': True
        },
        'features': {
            'manual_input': True,
            'file_upload': False,  # Removed
            'ocr_processing': False,  # Removed
            'prediction_confidence': True,
            'data_validation': True
        }
    }
    
    # Add warnings if models not loaded
    if not models_loaded:
        health_data['warnings'] = ['ML models not loaded - predictions unavailable']
    
    return jsonify(health_data)

@app.route('/', methods=['GET'])
def index():
    """Root endpoint with API information"""
    return jsonify({
        'message': 'CheckWise API v2.1.0 - Simplified',
        'status': 'running',
        'endpoints': {
            'health': '/api/health',
            'predict': '/api/predict (POST)',
            'diseases': '/api/diseases',
            'parameters': '/api/parameters'
        },
        'models_loaded': model is not None and label_encoder is not None,
        'description': 'Manual CBC parameter input for disease prediction'
    })

@app.route('/api/parameters', methods=['GET'])
def get_parameters():
    """Get comprehensive information about CBC parameters"""
    parameters = {
        'required': [
            'WBC', 'LY%', 'MO%', 'NE%', 'EO%', 'BA%', 'LY#', 'MO#', 'NE#', 'EO#', 'BA#',
            'RBC', 'HGB', 'HCT', 'MCV', 'MCHC', 'MCH', 'RDW', 'PLT', 'MPV', 'Age', 'Gender'
        ],
        'critical': ['WBC', 'RBC', 'HGB', 'HCT', 'PLT', 'Age', 'Gender'],
        'units': {
            'WBC': {'default': '10³/μL', 'alternatives': ['K/μL', 'cells/μL', '10⁹/L']},
            'RBC': {'default': '10⁶/μL', 'alternatives': ['M/μL', 'cells/μL', '10¹²/L']},
            'HGB': {'default': 'g/dL', 'alternatives': ['g/L', 'mmol/L']},
            'HCT': {'default': '%', 'alternatives': ['L/L', 'fraction']},
            'MCV': {'default': 'fL', 'alternatives': ['μm³']},
            'MCH': {'default': 'pg', 'alternatives': ['fmol']},
            'MCHC': {'default': 'g/dL', 'alternatives': ['g/L', 'mmol/L']},
            'RDW': {'default': '%', 'alternatives': ['CV%']},
            'PLT': {'default': '10³/μL', 'alternatives': ['K/μL', 'cells/μL', '10⁹/L']},
            'MPV': {'default': 'fL', 'alternatives': ['μm³']},
            'Age': {'default': 'years', 'alternatives': ['months', 'days']},
            'LY%': {'default': '%', 'alternatives': ['fraction']},
            'MO%': {'default': '%', 'alternatives': ['fraction']},
            'NE%': {'default': '%', 'alternatives': ['fraction']},
            'EO%': {'default': '%', 'alternatives': ['fraction']},
            'BA%': {'default': '%', 'alternatives': ['fraction']},
            'LY#': {'default': '10³/μL', 'alternatives': ['K/μL', 'cells/μL', '10⁹/L']},
            'MO#': {'default': '10³/μL', 'alternatives': ['K/μL', 'cells/μL', '10⁹/L']},
            'NE#': {'default': '10³/μL', 'alternatives': ['K/μL', 'cells/μL', '10⁹/L']},
            'EO#': {'default': '10³/μL', 'alternatives': ['K/μL', 'cells/μL', '10⁹/L']},
            'BA#': {'default': '10³/μL', 'alternatives': ['K/μL', 'cells/μL', '10⁹/L']}
        },
        'normal_ranges': {
            # Based on standard medical reference ranges
            'WBC': {'min': 4.0, 'max': 11.0, 'unit': '10³/μL', 'note': 'White Blood Cell Count'},
            'RBC': {'min': 4.2 if 'gender' == 1 else 3.8, 'max': 5.4 if 'gender' == 1 else 5.2, 'unit': '10⁶/μL', 'note': 'Red Blood Cell Count (varies by gender)'},
            'HGB': {'min': 13.5 if 'gender' == 1 else 12.0, 'max': 17.5 if 'gender' == 1 else 15.5, 'unit': 'g/dL', 'note': 'Hemoglobin (varies by gender)'},
            'HCT': {'min': 41.0 if 'gender' == 1 else 36.0, 'max': 50.0 if 'gender' == 1 else 44.0, 'unit': '%', 'note': 'Hematocrit (varies by gender)'},
            'MCV': {'min': 80.0, 'max': 100.0, 'unit': 'fL', 'note': 'Mean Corpuscular Volume'},
            'MCH': {'min': 27.0, 'max': 33.0, 'unit': 'pg', 'note': 'Mean Corpuscular Hemoglobin'},
            'MCHC': {'min': 32.0, 'max': 36.0, 'unit': 'g/dL', 'note': 'Mean Corpuscular Hemoglobin Concentration'},
            'RDW': {'min': 11.5, 'max': 14.5, 'unit': '%', 'note': 'Red Cell Distribution Width'},
            'PLT': {'min': 150.0, 'max': 450.0, 'unit': '10³/μL', 'note': 'Platelet Count'},
            'MPV': {'min': 7.5, 'max': 11.5, 'unit': 'fL', 'note': 'Mean Platelet Volume'},
            'LY%': {'min': 20.0, 'max': 40.0, 'unit': '%', 'note': 'Lymphocyte Percentage'},
            'MO%': {'min': 2.0, 'max': 8.0, 'unit': '%', 'note': 'Monocyte Percentage'},
            'NE%': {'min': 50.0, 'max': 70.0, 'unit': '%', 'note': 'Neutrophil Percentage'},
            'EO%': {'min': 1.0, 'max': 4.0, 'unit': '%', 'note': 'Eosinophil Percentage'},
            'BA%': {'min': 0.0, 'max': 1.0, 'unit': '%', 'note': 'Basophil Percentage'},
            'LY#': {'min': 1.2, 'max': 3.4, 'unit': '10³/μL', 'note': 'Lymphocyte Absolute Count'},
            'MO#': {'min': 0.1, 'max': 0.9, 'unit': '10³/μL', 'note': 'Monocyte Absolute Count'},
            'NE#': {'min': 1.8, 'max': 7.7, 'unit': '10³/μL', 'note': 'Neutrophil Absolute Count'},
            'EO#': {'min': 0.05, 'max': 0.5, 'unit': '10³/μL', 'note': 'Eosinophil Absolute Count'},
            'BA#': {'min': 0.0, 'max': 0.2, 'unit': '10³/μL', 'note': 'Basophil Absolute Count'},
            'Age': {'min': 0.0, 'max': 120.0, 'unit': 'years', 'note': 'Patient Age'},
            'Gender': {'min': 0, 'max': 1, 'description': '0=Female, 1=Male', 'note': 'Patient Gender'}
        },
        'descriptions': {
            'WBC': 'White Blood Cell Count - measures infection-fighting cells',
            'RBC': 'Red Blood Cell Count - measures oxygen-carrying cells',
            'HGB': 'Hemoglobin - protein that carries oxygen',
            'HCT': 'Hematocrit - percentage of blood volume made up by RBCs',
            'PLT': 'Platelet Count - measures blood clotting cells',
            'Age': 'Patient age in years',
            'Gender': 'Patient gender (0=Female, 1=Male)'
        }
    }
    return jsonify(parameters)

@app.route('/api/convert', methods=['POST'])
def convert_units():
    """Convert CBC parameter values between different units"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        parameter = data.get('parameter')
        value = data.get('value')
        from_unit = data.get('from_unit')
        to_unit = data.get('to_unit', 'default')
        
        if not all([parameter, value is not None, from_unit]):
            return jsonify({'error': 'Missing required fields: parameter, value, from_unit'}), 400
        
        try:
            value = float(value)
        except ValueError:
            return jsonify({'error': 'Value must be a number'}), 400
        
        # Convert to default unit first
        converted_value = convert_to_default_unit(parameter, value, from_unit)
        
        return jsonify({
            'parameter': parameter,
            'original_value': value,
            'original_unit': from_unit,
            'converted_value': converted_value,
            'converted_unit': 'default',
            'success': True
        })
        
    except Exception as e:
        return jsonify({'error': f'Conversion failed: {str(e)}'}), 500

@app.route('/api/validate', methods=['POST'])
def validate_input():
    """Validate input parameters without making a prediction"""
    try:
        data = request.json
        if not data:
            return jsonify({
                'error': 'No data provided for validation',
                'success': False
            }), 400
        
        validation_result = validate_and_process_input(data)
        
        return jsonify({
            'validation': validation_result,
            'success': True,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        return jsonify({
            'error': 'Validation failed',
            'success': False
        }), 500



@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found', 'success': False}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error', 'success': False}), 500

if __name__ == '__main__':
    # Try to load models at startup
    logger.info("Starting CheckWise API...")
    load_models()
    
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting server on port {port}, debug={debug_mode}")
    app.run(host='0.0.0.0', debug=debug_mode, port=port)