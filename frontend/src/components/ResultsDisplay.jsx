import React from 'react';

const ResultsDisplay = ({ results }) => {
  if (!results || !results.top_predictions) {
    return null;
  }

  const { prediction, top_predictions, data_quality, analysis } = results;

  return (
    <div className="p-6 mt-8 bg-white rounded-lg shadow-lg">
      <h2 className="mb-6 text-2xl font-bold text-gray-800">Diagnosis Results</h2>
      
      <div className="p-4 mb-6 border-l-4 border-blue-500 rounded-lg bg-blue-50">
        <h3 className="mb-2 text-lg font-semibold text-blue-800">Primary Diagnosis</h3>
        <p className="text-xl font-bold text-blue-900">{prediction}</p>
      </div>

      <div className="mb-6">
        <h3 className="mb-3 text-lg font-semibold text-gray-800">Confidence Scores</h3>
        <div className="space-y-2">
          {top_predictions.map((pred, index) => (
            <div key={index} className="flex items-center justify-between p-3 rounded bg-gray-50">
              <span className="font-medium text-gray-700">{pred.disease}</span>
              <span className="text-sm font-semibold text-blue-600">
                {(pred.probability * 100).toFixed(1)}%
              </span>
            </div>
          ))}
        </div>
      </div>

      <div className="p-4 mt-6 border-l-4 border-red-400 bg-red-50">
        <p className="text-sm text-red-700">
          <strong>Disclaimer:</strong> This analysis is for educational purposes only.
        </p>
      </div>
    </div>
  );
};

export default ResultsDisplay;
