import React from 'react';
import { AnalysisResult } from '../../types';

interface AnalysisResultsProps {
  results: AnalysisResult[];
  isLoading?: boolean;
}

const AnalysisResults: React.FC<AnalysisResultsProps> = ({ results, isLoading = false }) => {
  if (isLoading) {
    return (
      <div className="space-y-4">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="space-y-3">
            <div className="h-4 bg-gray-200 rounded"></div>
            <div className="h-4 bg-gray-200 rounded w-5/6"></div>
            <div className="h-4 bg-gray-200 rounded w-4/6"></div>
          </div>
        </div>
      </div>
    );
  }

  if (results.length === 0) {
    return (
      <div className="text-center py-8">
        <div className="text-gray-400 mb-4">
          <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <h3 className="text-lg font-medium text-gray-900 mb-2">No analysis results yet</h3>
        <p className="text-gray-500">Upload a video to get started with analysis</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {results.map((result) => (
        <div key={result.id} className="bg-white rounded-lg shadow-md border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-3">
              <div className={`w-3 h-3 rounded-full ${
                result.status === 'completed' ? 'bg-green-500' :
                result.status === 'processing' ? 'bg-yellow-500' :
                result.status === 'error' ? 'bg-red-500' : 'bg-gray-500'
              }`}></div>
              <span className="text-sm font-medium text-gray-900 capitalize">
                {result.status}
              </span>
              {result.progress && result.status === 'processing' && (
                <span className="text-sm text-gray-500">
                  {result.progress}%
                </span>
              )}
            </div>
            <span className="text-sm text-gray-500">
              {new Date(result.createdAt).toLocaleDateString()}
            </span>
          </div>

          {result.status === 'completed' && result.result && (
            <div className="space-y-4">
              {/* Summary */}
              <div>
                <h4 className="text-lg font-semibold text-gray-900 mb-2">Summary</h4>
                <p className="text-gray-700 leading-relaxed">{result.result.summary}</p>
              </div>

              {/* Key Points */}
              {result.result.keyPoints && result.result.keyPoints.length > 0 && (
                <div>
                  <h4 className="text-lg font-semibold text-gray-900 mb-2">Key Points</h4>
                  <ul className="space-y-2">
                    {result.result.keyPoints.map((point, index) => (
                      <li key={index} className="flex items-start space-x-2">
                        <span className="text-blue-500 mt-1">•</span>
                        <span className="text-gray-700">{point}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Sentiment */}
              <div>
                <h4 className="text-lg font-semibold text-gray-900 mb-2">Sentiment</h4>
                <div className="flex items-center space-x-2">
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                    result.result.sentiment === 'positive' ? 'bg-green-100 text-green-800' :
                    result.result.sentiment === 'negative' ? 'bg-red-100 text-red-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {result.result.sentiment}
                  </span>
                </div>
              </div>

              {/* Duration */}
              <div>
                <h4 className="text-lg font-semibold text-gray-900 mb-2">Duration</h4>
                <p className="text-gray-700">
                  {Math.floor(result.result.duration / 60)}:{(result.result.duration % 60).toString().padStart(2, '0')}
                </p>
              </div>

              {/* Language */}
              {result.result.language && (
                <div>
                  <h4 className="text-lg font-semibold text-gray-900 mb-2">Language</h4>
                  <p className="text-gray-700">{result.result.language}</p>
                </div>
              )}
            </div>
          )}

          {result.status === 'error' && result.error && (
            <div className="bg-red-50 border border-red-200 rounded-md p-4">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-red-800">Analysis failed</h3>
                  <div className="mt-2 text-sm text-red-700">
                    <p>{result.error}</p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default AnalysisResults; 