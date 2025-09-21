import { useState, useEffect } from 'react';
import axios from 'axios';

const DiagnosisForm = ({ onResult }) => {
  const [formData, setFormData] = useState({
    WBC: 7.5,
    'LY%': 30,
    'MO%': 7,
    'NE%': 60,
    'EO%': 2,
    'BA%': 1,
    'LY#': 2.2,
    'MO#': 0.5,
    'NE#': 4.5,
    'EO#': 0.15,
    'BA#': 0.07,
    RBC: 4.8,
    HGB: 14,
    HCT: 42,
    MCV: 88,
    MCHC: 33,
    MCH: 29,
    RDW: 13,
    PLT: 250,
    MPV: 10,
    Age: 35,
    Gender: 1 // 1 for Male, 0 for Female
  });
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [validationResults, setValidationResults] = useState(null);
  const [parameters, setParameters] = useState(null);
  const [selectedUnits, setSelectedUnits] = useState({});
  
  // Fetch parameter information on component mount
  useEffect(() => {
    const fetchParameters = async () => {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/api/parameters`);
        setParameters(response.data);
      } catch (err) {
        console.error('Failed to fetch parameters:', err);
      }
    };
    
    fetchParameters();
  }, []);
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value === '' ? null : value
    });
    
    // Clear previous validation results when form changes
    setValidationResults(null);
    setError('');
  };
  
  const validateInput = async () => {
    try {
      const response = await axios.post(
        `${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/api/validate`,
        formData
      );
      
      if (response.data.success) {
        setValidationResults(response.data.validation);
        return response.data.validation.success;
      }
      return false;
    } catch (err) {
      console.error('Validation failed:', err);
      return false;
    }
  };
  
  const clearForm = () => {
    const resetFormData = {
      WBC: '', 'LY%': '', 'MO%': '', 'NE%': '', 'EO%': '', 'BA%': '',
      'LY#': '', 'MO#': '', 'NE#': '', 'EO#': '', 'BA#': '',
      RBC: '', HGB: '', HCT: '', MCV: '', MCHC: '', MCH: '',
      RDW: '', PLT: '', MPV: '', Age: '', Gender: ''
    };
    setFormData(resetFormData);
    setValidationResults(null);
    setError('');
  };
  
  const loadSampleData = () => {
    const sampleData = {
      WBC: 7.5, 'LY%': 30, 'MO%': 7, 'NE%': 60, 'EO%': 2, 'BA%': 1,
      'LY#': 2.2, 'MO#': 0.5, 'NE#': 4.5, 'EO#': 0.15, 'BA#': 0.07,
      RBC: 4.8, HGB: 14, HCT: 42, MCV: 88, MCHC: 33, MCH: 29,
      RDW: 13, PLT: 250, MPV: 10, Age: 35, Gender: 1
    };
    setFormData(sampleData);
    setValidationResults(null);
    setError('');
  };
  
  const isParameterOutOfRange = (paramName, value) => {
    if (!parameters || !parameters.normal_ranges || !value) return false;
    const range = parameters.normal_ranges[paramName];
    if (!range) return false;
    const numValue = parseFloat(value);
    return numValue < range.min || numValue > range.max;
  };
  
  const getParameterStatus = (paramName, value) => {
    if (!value || value === '') return 'empty';
    if (isParameterOutOfRange(paramName, value)) return 'warning';
    return 'normal';
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      // First validate the input
      const isValid = await validateInput();
      if (!isValid) {
        setError('Please check your input data. Some parameters may be missing or invalid.');
        setLoading(false);
        return;
      }
      
      const response = await axios.post(
        `${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/api/predict`, 
        formData
      );
      
      if (response.data.success) {
        onResult(response.data);
      } else {
        setError(response.data.error || 'Prediction failed');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred during prediction');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
      <div className="bg-gradient-to-r from-blue-600 to-indigo-600 px-8 py-6">
        <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center">
          <div className="mb-4 sm:mb-0">
            <h2 className="text-2xl font-bold text-white mb-2">CBC Parameters Input</h2>
            <p className="text-blue-100 text-sm">Enter your Complete Blood Count test results with automatic unit conversion</p>
          </div>
          <div className="flex space-x-2">
            <button
              type="button"
              onClick={loadSampleData}
              className="bg-white bg-opacity-20 hover:bg-opacity-30 text-white px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 flex items-center"
            >
              Load Sample
            </button>
            <button
              type="button"
              onClick={clearForm}
              className="bg-white bg-opacity-20 hover:bg-opacity-30 text-white px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 flex items-center"
            >
              <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
              Clear All
            </button>
          </div>
        </div>
      </div>
      <div className="p-8">
      
      {/* Instructions */}
      <div className="mb-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
        <h3 className="text-lg font-semibold mb-2 text-blue-800">How to Use</h3>
        <ul className="text-sm text-blue-700 space-y-1">
          <li>• Enter your Complete Blood Count (CBC) test results in the fields below</li>
          <li>• Critical parameters are marked with * and are required for accurate prediction</li>
          <li>• Values outside normal ranges will be highlighted in orange</li>
          <li>• Click "Load Sample" to see example values</li>
        </ul>
      </div>
      
      {/* Validation Results */}
      {validationResults && !validationResults.success && (
        <div className="mb-6 p-4 bg-yellow-50 rounded-lg border border-yellow-200">
          <h4 className="font-semibold text-yellow-800 mb-2">Input Validation</h4>
          {validationResults.data_quality && (
            <div className="text-sm text-yellow-700">
              <p>Data Completeness: {validationResults.data_quality.completeness_percentage}%</p>
              {validationResults.data_quality.critical_missing.length > 0 && (
                <p>Missing Critical Parameters: {validationResults.data_quality.critical_missing.join(', ')}</p>
              )}
            </div>
          )}
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Critical Parameters Section */}
        <div className="mb-8">
          <h3 className="text-lg font-semibold mb-4 text-gray-700 border-b pb-2">
            Critical Parameters *
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {parameters?.critical?.map((key) => (
              <div key={key} className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {key === 'Gender' ? 'Gender (1=M, 0=F)' : key}
                  <span className="text-red-500">*</span>
                </label>
                <div className="flex space-x-2">
                  <input
                    type="number"
                    step={key === 'Gender' ? '1' : '0.01'}
                    name={key}
                    value={formData[key] || ''}
                    onChange={handleChange}
                    placeholder="Enter value"
                    className={`flex-1 px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                      getParameterStatus(key, formData[key]) === 'empty' 
                        ? 'border-red-300 bg-red-50' 
                        : getParameterStatus(key, formData[key]) === 'warning'
                        ? 'border-orange-300 bg-orange-50'
                        : 'border-gray-300'
                    }`}
                  />
                  {parameters?.units?.[key]?.alternatives && (
                    <select
                      value={selectedUnits[key] || parameters.units[key].default}
                      onChange={(e) => setSelectedUnits({...selectedUnits, [key]: e.target.value})}
                      className="px-2 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value={parameters.units[key].default}>
                        {parameters.units[key].default}
                      </option>
                      {parameters.units[key].alternatives.map(unit => (
                        <option key={unit} value={unit}>{unit}</option>
                      ))}
                    </select>
                  )}
                </div>
                {parameters?.normal_ranges?.[key] && (
                  <div className="text-xs text-gray-500 mt-1">
                    Normal: {parameters.normal_ranges[key].min} - {parameters.normal_ranges[key].max} {parameters.normal_ranges[key].unit}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Optional Parameters Section */}
        <div className="mb-8">
          <h3 className="text-lg font-semibold mb-4 text-gray-700 border-b pb-2">
            Additional Parameters (Optional)
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {Object.keys(formData)
              .filter(key => !parameters?.critical?.includes(key))
              .map((key) => (
              <div key={key} className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {key}
                </label>
                <div className="flex space-x-2">
                  <input
                    type="number"
                    step="0.01"
                    name={key}
                    value={formData[key] || ''}
                    onChange={handleChange}
                    placeholder="Enter value"
                    className={`flex-1 px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                      getParameterStatus(key, formData[key]) === 'warning'
                        ? 'border-orange-300 bg-orange-50'
                        : 'border-gray-300'
                    }`}
                  />
                  {parameters?.units?.[key]?.alternatives && (
                    <select
                      value={selectedUnits[key] || parameters.units[key].default}
                      onChange={(e) => setSelectedUnits({...selectedUnits, [key]: e.target.value})}
                      className="px-2 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value={parameters.units[key].default}>
                        {parameters.units[key].default}
                      </option>
                      {parameters.units[key].alternatives.map(unit => (
                        <option key={unit} value={unit}>{unit}</option>
                      ))}
                    </select>
                  )}
                </div>
                {parameters?.normal_ranges?.[key] && (
                  <div className="text-xs text-gray-500 mt-1">
                    Normal: {parameters.normal_ranges[key].min} - {parameters.normal_ranges[key].max} {parameters.normal_ranges[key].unit}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
        
        {error && (
          <div className="bg-red-50 p-4 rounded-md text-red-600 mb-4">
            <div className="flex items-center">
              <svg className="h-5 w-5 text-red-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
              {error}
            </div>
          </div>
        )}
        
        <div className="flex justify-center">
          <button
            type="submit"
            disabled={loading}
            className="bg-blue-600 text-white px-8 py-3 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-semibold text-lg"
          >
            {loading ? (
              <div className="flex items-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Analyzing...
              </div>
            ) : 'Analyze CBC Results'}
          </button>
        </div>
      </form>
      </div>
    </div>
  );
};

export default DiagnosisForm;