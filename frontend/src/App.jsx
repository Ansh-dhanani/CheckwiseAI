import { useState } from 'react'
import DiagnosisForm from './components/DiagnosisForm'
import ResultsDisplay from './components/ResultsDisplay'
import About from './components/About'

function App() {
  const [results, setResults] = useState(null);
  const [currentPage, setCurrentPage] = useState('home');

  const NavigationBar = () => (
    <nav className="bg-white shadow-lg">
      <div className="px-4 mx-auto max-w-7xl sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <div className="flex items-center flex-shrink-0">
              <div className="flex items-center justify-center w-8 h-8 mr-3 bg-blue-600 rounded-lg">
                <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h1 className="text-xl font-bold text-gray-900">CheckwiseAI</h1>
            </div>
          </div>
          <div className="flex space-x-4">
            <button
              onClick={() => {setCurrentPage('home'); setResults(null);}}
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
                currentPage === 'home' 
                  ? 'bg-blue-100 text-blue-700' 
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
              }`}
            >
              CBC Analysis
            </button>
            <button
              onClick={() => setCurrentPage('about')}
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
                currentPage === 'about' 
                  ? 'bg-blue-100 text-blue-700' 
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
              }`}
            >
              About
            </button>
          </div>
        </div>
      </div>
    </nav>
  );

  if (currentPage === 'about') {
    return (
      <div>
        <NavigationBar />
        <About />
      </div>
    );
  }

  return (
    <div>
      <NavigationBar />
      <div className="min-h-screen px-4 py-12 bg-gradient-to-br from-blue-50 to-indigo-100 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-7xl">
          <div className="mb-12 text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 mb-6 bg-blue-600 rounded-full shadow-lg">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <h1 className="mb-4 text-4xl font-bold text-gray-900">CBC Analysis Tool</h1>
            <p className="max-w-2xl mx-auto mb-2 text-xl text-gray-600">
              Advanced AI-powered Complete Blood Count analysis with comprehensive diagnostic insights
            </p>
            <p className="text-sm font-medium text-blue-600">
              ✨ Enhanced with unit conversion and real-time validation
            </p>
          </div>
          
          <DiagnosisForm onResult={setResults} />
          
          {results && (
            <div className="mt-8">
              <ResultsDisplay results={results} />
            </div>
          )}
          
          <div className="mt-12 text-center">
            <div className="max-w-2xl p-6 mx-auto bg-white rounded-lg shadow-md">
              <div className="flex items-center justify-center mb-3">
                <svg className="w-5 h-5 mr-2 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.732 15.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
                <span className="font-semibold text-gray-900">Medical Disclaimer</span>
              </div>
              <p className="text-sm leading-relaxed text-gray-600">
                This tool is designed for educational purposes and to assist healthcare professionals. 
                It should never replace professional medical diagnosis, treatment, or consultation with qualified healthcare providers.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App