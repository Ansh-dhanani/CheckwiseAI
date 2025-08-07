import { useState } from 'react';
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
  const [uploadLoading, setUploadLoading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState('');
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };
  
  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    setUploadLoading(true);
    setUploadMessage('');
    setError('');
    
    const formDataUpload = new FormData();
    formDataUpload.append('file', file);
    
    try {
      const response = await axios.post(
        `${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/api/upload`,
        formDataUpload,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      );
      
      if (response.data.success) {
        const extractedData = response.data.extracted_data;
        // Reset all form data to null first
        const resetFormData = {
          WBC: null, 'LY%': null, 'MO%': null, 'NE%': null, 'EO%': null, 'BA%': null,
          'LY#': null, 'MO#': null, 'NE#': null, 'EO#': null, 'BA#': null,
          RBC: null, HGB: null, HCT: null, MCV: null, MCHC: null, MCH: null,
          RDW: null, PLT: null, MPV: null, Age: null, Gender: null
        };
        // Replace with extracted data only
        setFormData({ ...resetFormData, ...extractedData });
        setUploadMessage(`Extracted ${Object.keys(extractedData).length} parameters. Missing values set to null.`);
      } else {
        setError(response.data.error || 'File upload failed');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'File upload error');
    } finally {
      setUploadLoading(false);
    }
  };
  
  const clearForm = () => {
    const resetFormData = {
      WBC: null, 'LY%': null, 'MO%': null, 'NE%': null, 'EO%': null, 'BA%': null,
      'LY#': null, 'MO#': null, 'NE#': null, 'EO#': null, 'BA#': null,
      RBC: null, HGB: null, HCT: null, MCV: null, MCHC: null, MCH: null,
      RDW: null, PLT: null, MPV: null, Age: null, Gender: null
    };
    setFormData(resetFormData);
    setUploadMessage('');
    setError('');
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      const response = await axios.post(`${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/api/predict`, formData);
      if (response.data.success) {
        onResult(response.data);
      } else {
        setError('Prediction failed');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">CBC Test Results</h2>
      
      {/* File Upload Section */}
      <div className="mb-6 p-4 bg-gray-50 rounded-lg">
        <h3 className="text-lg font-semibold mb-3 text-gray-700">Upload Medical Report</h3>
        <p className="text-sm text-gray-600 mb-3">Upload PDF, Image (JPG/PNG), or CSV/Excel file to auto-fill the form</p>
        <input
          type="file"
          accept=".pdf,.jpg,.jpeg,.png,.csv,.xlsx,.xls"
          onChange={handleFileUpload}
          disabled={uploadLoading}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        {uploadLoading && (
          <div className="mt-2 text-blue-600">
            <span className="inline-block animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></span>
            Processing file...
          </div>
        )}
        {uploadMessage && (
          <div className="mt-2 text-green-600 text-sm">
            {uploadMessage}
          </div>
        )}
      </div>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {Object.keys(formData).map((key) => (
            <div key={key} className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                {key === 'Gender' ? 'Gender (1=Male, 0=Female)' : key}
              </label>
              <input
                type="number"
                step="0.01"
                name={key}
                value={formData[key] || ''}
                onChange={handleChange}
                placeholder={formData[key] === null ? 'Not extracted' : ''}
                className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                  formData[key] === null ? 'border-red-300 bg-red-50' : 'border-gray-300'
                }`}
              />
            </div>
          ))}
        </div>
        
        {error && (
          <div className="bg-red-50 p-4 rounded-md text-red-600 mb-4">
            {error}
          </div>
        )}
        
        <div className="flex justify-between">
          <button
            type="button"
            onClick={clearForm}
            className="bg-gray-500 text-white px-6 py-2 rounded-md hover:bg-gray-600"
          >
            Clear Form
          </button>
          <button
            type="submit"
            disabled={loading}
            className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Processing...' : 'Diagnose'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default DiagnosisForm;