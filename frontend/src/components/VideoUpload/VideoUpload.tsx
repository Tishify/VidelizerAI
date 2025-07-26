import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { VideoFile } from '../../types';
import { validateVideoFile, createVideoFile, generateVideoPreview } from '../../services/fileUpload';
import LoadingSpinner from '../LoadingSpinner/LoadingSpinner';

interface VideoUploadProps {
  onVideoSelect: (videoFile: VideoFile) => void;
  onError: (error: string) => void;
  disabled?: boolean;
}

const VideoUpload: React.FC<VideoUploadProps> = ({
  onVideoSelect,
  onError,
  disabled = false,
}) => {
  const [isGeneratingPreview, setIsGeneratingPreview] = useState(false);

  const onDrop = useCallback(
    async (acceptedFiles: File[]) => {
      if (acceptedFiles.length === 0) return;

      const file = acceptedFiles[0];
      const validation = validateVideoFile(file);

      if (!validation.isValid) {
        onError(validation.error!);
        return;
      }

      try {
        setIsGeneratingPreview(true);
        const videoFile = createVideoFile(file);
        
        // Generate preview
        try {
          const preview = await generateVideoPreview(file);
          videoFile.preview = preview;
        } catch (error) {
          console.warn('Could not generate preview:', error);
        }

        onVideoSelect(videoFile);
      } catch (error) {
        onError('Failed to process video file');
      } finally {
        setIsGeneratingPreview(false);
      }
    },
    [onVideoSelect, onError]
  );

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: {
      'video/*': ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm']
    },
    multiple: false,
    disabled,
  });

  const getDropzoneClasses = () => {
    let baseClasses = 'border-2 border-dashed rounded-lg p-8 text-center transition-all duration-200 cursor-pointer';
    
    if (disabled) {
      return `${baseClasses} border-gray-300 bg-gray-50 cursor-not-allowed`;
    }
    
    if (isDragReject) {
      return `${baseClasses} border-red-400 bg-red-50 text-red-600`;
    }
    
    if (isDragActive) {
      return `${baseClasses} border-blue-400 bg-blue-50 text-blue-600`;
    }
    
    return `${baseClasses} border-gray-300 hover:border-blue-400 hover:bg-blue-50`;
  };

  return (
    <div className="w-full">
      <div {...getRootProps()} className={getDropzoneClasses()}>
        <input {...getInputProps()} />
        
        {isGeneratingPreview ? (
          <LoadingSpinner 
            size="lg" 
            text="Processing video..." 
            className="py-8"
          />
        ) : (
          <div className="space-y-4">
            <div className="mx-auto w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center">
              <svg
                className="w-8 h-8 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M7 4v16l13-8z"
                />
              </svg>
            </div>
            
            <div>
              <p className="text-lg font-medium text-gray-900">
                {isDragActive ? 'Drop your video here' : 'Upload your video'}
              </p>
              <p className="text-sm text-gray-500 mt-1">
                Drag and drop your video file here, or click to browse
              </p>
              <p className="text-xs text-gray-400 mt-2">
                Supported formats: MP4, AVI, MOV, WMV, FLV, WebM (max 500MB)
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default VideoUpload; 