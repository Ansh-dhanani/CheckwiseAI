import { useState } from 'react'
import DiagnosisForm from './components/DiagnosisForm'
import ResultsDisplay from './components/ResultsDisplay'

function App() {
  const [results, setResults] = useState(null);

  return (
    <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">CheckWise - CBC Analysis</h1>
          <p className="text-xl text-gray-600">
            Manual CBC parameter input for AI-powered disease prediction analysis
          </p>
          <p className="text-sm text-gray-500 mt-2">
            Simplified interface - No file uploads required
          </p>
        </div>
        
        <DiagnosisForm onResult={setResults} />
        
        {results && <ResultsDisplay results={results} />}
        
        <div className="mt-12 text-center text-gray-500 text-sm">
          <p>This tool is for educational purposes only. Always consult with a healthcare professional.</p>
        </div>
      </div>
    </div>
  )
}

export default App