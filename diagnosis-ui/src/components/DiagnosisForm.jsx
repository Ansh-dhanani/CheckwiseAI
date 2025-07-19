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
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
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
                value={formData[key]}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
          ))}
        </div>
        
        {error && (
          <div className="bg-red-50 p-4 rounded-md text-red-600 mb-4">
            {error}
          </div>
        )}
        
        <div className="flex justify-end">
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