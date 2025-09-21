import React from 'react';

const About = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        {/* Header Section */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-600 rounded-full mb-6">
            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-4">About CheckwiseAI</h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            An AI-powered Complete Blood Count (CBC) analysis tool that helps healthcare professionals and students understand blood test results.
          </p>
        </div>

        {/* Main Content */}
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
          {/* What is CheckwiseAI */}
          <div className="p-8 border-b border-gray-100">
            <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center">
              <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center mr-3">
                <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              What is CheckwiseAI?
            </h2>
            <p className="text-gray-700 leading-relaxed mb-4">
              CheckwiseAI is an advanced machine learning system designed to analyze Complete Blood Count (CBC) parameters and provide preliminary diagnostic insights. Our AI model has been trained on extensive medical datasets to recognize patterns in blood work that may indicate various health conditions.
            </p>
            <div className="bg-blue-50 border-l-4 border-blue-400 p-4 rounded-r-lg">
              <p className="text-blue-800 font-medium">
                <strong>Important:</strong> This tool is designed for educational purposes and to assist healthcare professionals. It should never replace professional medical diagnosis or treatment.
              </p>
            </div>
          </div>

          {/* How it Works */}
          <div className="p-8 border-b border-gray-100">
            <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
              <div className="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center mr-3">
                <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              How It Works
            </h2>
            <div className="grid md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-blue-600 font-bold text-lg">1</span>
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Input CBC Values</h3>
                <p className="text-gray-600 text-sm">Enter your Complete Blood Count parameters with support for multiple units</p>
              </div>
              <div className="text-center">
                <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-green-600 font-bold text-lg">2</span>
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">AI Analysis</h3>
                <p className="text-gray-600 text-sm">Advanced machine learning algorithms analyze patterns in your blood work</p>
              </div>
              <div className="text-center">
                <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-purple-600 font-bold text-lg">3</span>
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Get Insights</h3>
                <p className="text-gray-600 text-sm">Receive detailed analysis with confidence scores and recommendations</p>
              </div>
            </div>
          </div>

          {/* Features */}
          <div className="p-8 border-b border-gray-100">
            <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
              <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center mr-3">
                <svg className="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
                </svg>
              </div>
              Key Features
            </h2>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0 w-6 h-6 bg-green-100 rounded-full flex items-center justify-center mt-1">
                  <svg className="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900">Multiple Unit Support</h3>
                  <p className="text-gray-600 text-sm">Convert between different measurement units automatically</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0 w-6 h-6 bg-green-100 rounded-full flex items-center justify-center mt-1">
                  <svg className="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900">Real-time Validation</h3>
                  <p className="text-gray-600 text-sm">Instant feedback on parameter ranges and data quality</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0 w-6 h-6 bg-green-100 rounded-full flex items-center justify-center mt-1">
                  <svg className="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900">Comprehensive Analysis</h3>
                  <p className="text-gray-600 text-sm">Detailed insights with confidence scores and recommendations</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0 w-6 h-6 bg-green-100 rounded-full flex items-center justify-center mt-1">
                  <svg className="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900">Educational Tool</h3>
                  <p className="text-gray-600 text-sm">Perfect for medical students and healthcare professionals</p>
                </div>
              </div>
            </div>
          </div>

          {/* Technology */}
          <div className="p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
              <div className="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center mr-3">
                <svg className="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              Technology Stack
            </h2>
            <div className="grid md:grid-cols-2 gap-8">
              <div>
                <h3 className="font-semibold text-gray-900 mb-3">Frontend</h3>
                <ul className="space-y-2 text-gray-600">
                  <li className="flex items-center"><span className="w-2 h-2 bg-blue-400 rounded-full mr-2"></span>React 18</li>
                  <li className="flex items-center"><span className="w-2 h-2 bg-blue-400 rounded-full mr-2"></span>Tailwind CSS</li>
                  <li className="flex items-center"><span className="w-2 h-2 bg-blue-400 rounded-full mr-2"></span>Vite Build System</li>
                  <li className="flex items-center"><span className="w-2 h-2 bg-blue-400 rounded-full mr-2"></span>Axios for API calls</li>
                </ul>
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-3">Backend</h3>
                <ul className="space-y-2 text-gray-600">
                  <li className="flex items-center"><span className="w-2 h-2 bg-green-400 rounded-full mr-2"></span>Python Flask API</li>
                  <li className="flex items-center"><span className="w-2 h-2 bg-green-400 rounded-full mr-2"></span>Scikit-learn ML Models</li>
                  <li className="flex items-center"><span className="w-2 h-2 bg-green-400 rounded-full mr-2"></span>NumPy & Pandas</li>
                  <li className="flex items-center"><span className="w-2 h-2 bg-green-400 rounded-full mr-2"></span>Advanced Data Validation</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        {/* Development Team */}
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden mt-8">
          <div className="p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
              <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center mr-3">
                <svg className="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              Development Team
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Backend Developer */}
              <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-6 border border-blue-200">
                <div className="text-center">
                  <div className="w-20 h-20 overflow-hidden rounded-full mx-auto mb-4 border-4 border-white shadow-lg">
                    <img 
                      className="w-full h-full object-cover" 
                      src="https://avatars.githubusercontent.com/u/187887332?v=4"
                      alt="Manan Panchal"
                    />
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 mb-1">Manan Panchal</h3>
                  <p className="text-blue-600 font-semibold mb-3">Backend Developer</p>
                  <div className="flex items-center justify-center space-x-2 text-gray-600">
                    <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                    </svg>
                    <a 
                      href="https://github.com/mananjp" 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-sm hover:text-blue-600 transition-colors"
                    >
                      github.com/mananjp
                    </a>
                  </div>
                </div>
              </div>

              {/* Frontend Developer */}
              <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl p-6 border border-purple-200">
                <div className="text-center">
                  <div className="w-20 h-20 overflow-hidden rounded-full mx-auto mb-4 border-4 border-white shadow-lg">
                    <img 
                      className="w-full h-full object-cover" 
                      src="https://avatars.githubusercontent.com/u/189432138?v=4"
                      alt="Ansh Dhanani"
                    />
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 mb-1">Ansh Dhanani</h3>
                  <p className="text-purple-600 font-semibold mb-3">Frontend Developer</p>
                  <div className="flex items-center justify-center space-x-2 text-gray-600">
                    <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                    </svg>
                    <a 
                      href="https://github.com/ansh-dhanani" 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-sm hover:text-purple-600 transition-colors"
                    >
                      github.com/ansh-dhanani
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-12">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Ready to analyze your CBC results?</h3>
            <p className="text-gray-600 mb-4">Get started with your Complete Blood Count analysis today.</p>
            <button 
              onClick={() => window.location.reload()} 
              className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-lg transition-colors duration-200"
            >
              Start Analysis
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;