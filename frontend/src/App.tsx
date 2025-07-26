import React, { useState } from 'react';
import UploadPage from './pages/UploadPage';
import ResultsPage from './pages/ResultsPage';
import './App.css';

function App() {
  const [currentPage, setCurrentPage] = useState<'upload' | 'results'>('upload');
  const [currentVideoId, setCurrentVideoId] = useState<string | undefined>();

  const handleNavigateToResults = (videoId: string) => {
    setCurrentVideoId(videoId);
    setCurrentPage('results');
  };

  const handleNavigateToUpload = () => {
    setCurrentPage('upload');
    setCurrentVideoId(undefined);
  };

  return (
    <div className="App">
      {/* Navigation Header */}
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-gray-900">VidelizerAI</h1>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={handleNavigateToUpload}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  currentPage === 'upload'
                    ? 'bg-blue-100 text-blue-800'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                }`}
              >
                Upload
              </button>
              <button
                onClick={() => handleNavigateToResults('demo-video-id')}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  currentPage === 'results'
                    ? 'bg-blue-100 text-blue-800'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                }`}
              >
                Results
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main>
        {currentPage === 'upload' ? (
          <UploadPage />
        ) : (
          <ResultsPage videoId={currentVideoId} />
        )}
      </main>
    </div>
  );
}

export default App;
