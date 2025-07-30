import React, { useState } from 'react';
import VideoUpload from '../components/VideoUpload/VideoUpload';
import LoadingSpinner from '../components/LoadingSpinner/LoadingSpinner';
import { VideoFile } from '../types';
import { videoApi } from '../services/api';
import { formatFileSize } from '../services/fileUpload';

const UploadPage: React.FC = () => {
  const [selectedVideo, setSelectedVideo] = useState<VideoFile | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [warning, setWarning] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleVideoSelect = (videoFile: VideoFile) => {
    setSelectedVideo(videoFile);
    setError(null);
    setWarning(null);
    setSuccess(null);
  };

  const handleError = (errorMessage: string) => {
    setError(errorMessage);
    setSelectedVideo(null);
  };

  const handleWarning = (warningMessage: string) => {
    setWarning(warningMessage);
  };

  const handleUpload = async () => {
    if (!selectedVideo) return;

    setIsUploading(true);
    setError(null);
    setSuccess(null);
    setUploadProgress(0);

    try {
      // Simulate upload progress
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return prev;
          }
          return prev + 10;
        });
      }, 200);

      // Upload the actual video file
      const response = await videoApi.uploadVideo(selectedVideo.file);
      
      clearInterval(progressInterval);
      setUploadProgress(100);

      if (response.success) {
        setSuccess('Video uploaded successfully! Analysis will begin shortly.');
        // You could navigate to results page here
        // navigate(`/results/${response.videoId}`);
      } else {
        setError(response.error || 'Upload failed');
      }
    } catch (error) {
      setError('Failed to upload video. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

  const handleRemoveVideo = () => {
    setSelectedVideo(null);
    setError(null);
    setSuccess(null);
    setUploadProgress(0);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Video Analysis
          </h1>
          <p className="text-lg text-gray-600">
            Upload your video to get AI-powered insights and analysis
          </p>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          {!selectedVideo ? (
            <VideoUpload
              onVideoSelect={handleVideoSelect}
              onError={handleError}
              onWarning={handleWarning}
              disabled={isUploading}
            />
          ) : (
            <div className="space-y-6">
              {/* Selected Video Preview */}
              <div className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-center space-x-4">
                  {selectedVideo.preview && (
                    <img
                      src={selectedVideo.preview}
                      alt="Video preview"
                      className="w-24 h-16 object-cover rounded"
                    />
                  )}
                  <div className="flex-1">
                    <h3 className="text-lg font-medium text-gray-900">
                      {selectedVideo.name}
                    </h3>
                    <p className="text-sm text-gray-500">
                      {formatFileSize(selectedVideo.size)}
                    </p>
                  </div>
                  <button
                    onClick={handleRemoveVideo}
                    className="text-red-600 hover:text-red-800 text-sm font-medium"
                  >
                    Remove
                  </button>
                </div>
              </div>

              {/* Upload Progress */}
              {isUploading && (
                <div className="space-y-2">
                  <div className="flex justify-between text-sm text-gray-600">
                    <span>Uploading...</span>
                    <span>{uploadProgress}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${uploadProgress}%` }}
                    ></div>
                  </div>
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex justify-center space-x-4">
                <button
                  onClick={handleUpload}
                  disabled={isUploading}
                  className="px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {isUploading ? (
                    <div className="flex items-center space-x-2">
                      <LoadingSpinner size="sm" color="white" />
                      <span>Uploading...</span>
                    </div>
                  ) : (
                    'Start Analysis'
                  )}
                </button>
              </div>
            </div>
          )}

          {/* Error Message */}
          {error && (
            <div className="mt-4 bg-red-50 border border-red-200 rounded-md p-4">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-red-800">Error</h3>
                  <div className="mt-2 text-sm text-red-700">
                    <p>{error}</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Warning Message */}
          {warning && (
            <div className="mt-4 bg-yellow-50 border border-yellow-200 rounded-md p-4">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-yellow-800">Warning</h3>
                  <div className="mt-2 text-sm text-yellow-700">
                    <p>{warning}</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Success Message */}
          {success && (
            <div className="mt-4 bg-green-50 border border-green-200 rounded-md p-4">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-green-800">Success</h3>
                  <div className="mt-2 text-sm text-green-700">
                    <p>{success}</p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default UploadPage; 