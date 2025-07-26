import { VideoFile } from '../types';

export const ACCEPTED_VIDEO_TYPES = {
  'video/mp4': ['.mp4'],
  'video/avi': ['.avi'],
  'video/mov': ['.mov'],
  'video/wmv': ['.wmv'],
  'video/flv': ['.flv'],
  'video/webm': ['.webm'],
};

export const MAX_FILE_SIZE = 500 * 1024 * 1024; // 500MB

export const validateVideoFile = (file: File): { isValid: boolean; error?: string } => {
  // Check file size
  if (file.size > MAX_FILE_SIZE) {
    return {
      isValid: false,
      error: `File size exceeds maximum limit of ${MAX_FILE_SIZE / (1024 * 1024)}MB`,
    };
  }

  // Check file type
  const isValidType = Object.keys(ACCEPTED_VIDEO_TYPES).includes(file.type);
  if (!isValidType) {
    return {
      isValid: false,
      error: 'Invalid file type. Please upload a video file (MP4, AVI, MOV, WMV, FLV, WebM)',
    };
  }

  return { isValid: true };
};

export const createVideoFile = (file: File): VideoFile => {
  return {
    id: `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
    name: file.name,
    size: file.size,
    type: file.type,
    lastModified: file.lastModified,
  };
};

export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

export const generateVideoPreview = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const video = document.createElement('video');
    video.preload = 'metadata';
    
    video.onloadedmetadata = () => {
      const canvas = document.createElement('canvas');
      const context = canvas.getContext('2d');
      
      if (!context) {
        reject(new Error('Could not get canvas context'));
        return;
      }
      
      canvas.width = 320;
      canvas.height = 180;
      
      // Seek to 1 second to get a frame
      video.currentTime = 1;
      
      video.onseeked = () => {
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const preview = canvas.toDataURL('image/jpeg', 0.8);
        resolve(preview);
      };
    };
    
    video.onerror = () => {
      reject(new Error('Could not load video for preview'));
    };
    
    video.src = URL.createObjectURL(file);
  });
}; 