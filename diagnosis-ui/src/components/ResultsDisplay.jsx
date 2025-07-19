import { useEffect, useRef } from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Pie } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend);

const ResultsDisplay = ({ results }) => {
  const chartRef = useRef(null);
  
  useEffect(() => {
    // Force chart update when results change
    if (chartRef.current) {
      chartRef.current.update();
    }
  }, [results]);
  
  if (!results || !results.top_predictions) {
    return null;
  }
  
  const { prediction, top_predictions } = results;
  
  // Prepare chart data
  const chartData = {
    labels: top_predictions.map(p => p.disease),
    datasets: [
      {
        data: top_predictions.map(p => p.probability * 100),
        backgroundColor: [
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 99, 132, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(75, 192, 192, 0.6)',
          'rgba(153, 102, 255, 0.6)',
        ],
        borderColor: [
          'rgba(54, 162, 235, 1)',
          'rgba(255, 99, 132, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)',
        ],
        borderWidth: 1,
      },
    ],
  };
  
  return (
    <div className="bg-white p-6 rounded-lg shadow-md mt-6">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">Diagnosis Results</h2>
      
      <div className="mb-6">
        <h3 className="text-xl font-semibold mb-2 text-gray-700">Primary Diagnosis</h3>
        <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
          <p className="text-2xl font-bold text-blue-700">{prediction}</p>
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h3 className="text-xl font-semibold mb-4 text-gray-700">Probability Distribution</h3>
          <div className="h-64">
            <Pie 
              ref={chartRef}
              data={chartData} 
              options={{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                  legend: {
                    position: 'bottom',
                  },
                  tooltip: {
                    callbacks: {
                      label: function(context) {
                        return `${context.label}: ${context.raw.toFixed(2)}%`;
                      }
                    }
                  }
                }
              }}
            />
          </div>
        </div>
        
        <div>
          <h3 className="text-xl font-semibold mb-4 text-gray-700">Top Predictions</h3>
          <div className="space-y-3">
            {top_predictions.map((pred, index) => (
              <div 
                key={index} 
                className={`p-3 rounded-lg ${
                  pred.disease === prediction 
                    ? 'bg-blue-50 border border-blue-200' 
                    : 'bg-gray-50 border border-gray-200'
                }`}
              >
                <div className="flex justify-between items-center">
                  <span className="font-medium">{pred.disease}</span>
                  <span className="font-bold">{(pred.probability * 100).toFixed(2)}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2.5 mt-2">
                  <div 
                    className={`h-2.5 rounded-full ${
                      pred.disease === prediction ? 'bg-blue-600' : 'bg-gray-500'
                    }`}
                    style={{ width: `${pred.probability * 100}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultsDisplay;