import { VideoFile } from '../types';

export const ACCEPTED_VIDEO_TYPES = {
  'video/mp4': ['.mp4'],
  'video/avi': ['.avi'],
  'video/mov': ['.mov'],
  'video/wmv': ['.wmv'],
  'video/flv': ['.flv'],
  'video/webm': ['.webm'],
};

export const ACCEPTED_EXTENSIONS = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm'];

export const MAX_FILE_SIZE = 500 * 1024 * 1024; // 500MB
export const MIN_FILE_SIZE = 1024; // 1KB minimum

export const validateVideoFile = (file: File): { isValid: boolean; error?: string } => {
  // Check if file exists
  if (!file) {
    return {
      isValid: false,
      error: 'No file selected',
    };
  }

  // Check file size - minimum
  if (file.size < MIN_FILE_SIZE) {
    return {
      isValid: false,
      error: 'File is too small. Please select a valid video file.',
    };
  }

  // Check file size - maximum
  if (file.size > MAX_FILE_SIZE) {
    return {
      isValid: false,
      error: `File size (${formatFileSize(file.size)}) exceeds maximum limit of ${formatFileSize(MAX_FILE_SIZE)}`,
    };
  }

  // Check file type using MIME type
  const isValidMimeType = Object.keys(ACCEPTED_VIDEO_TYPES).includes(file.type);
  if (!isValidMimeType) {
    return {
      isValid: false,
      error: `Invalid file type "${file.type}". Please upload a video file (MP4, AVI, MOV, WMV, FLV, WebM)`,
    };
  }

  // Check file extension as additional validation
  const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase();
  const isValidExtension = ACCEPTED_EXTENSIONS.includes(fileExtension);
  if (!isValidExtension) {
    return {
      isValid: false,
      error: `Invalid file extension "${fileExtension}". Please upload a video file (MP4, AVI, MOV, WMV, FLV, WebM)`,
    };
  }

  // Check if file name is valid
  if (!file.name || file.name.trim().length === 0) {
    return {
      isValid: false,
      error: 'Invalid file name',
    };
  }

  // Check for special characters in filename that might cause issues
  const invalidChars = /[<>:"/\\|?*]/;
  if (invalidChars.test(file.name)) {
    return {
      isValid: false,
      error: 'File name contains invalid characters. Please rename the file and try again.',
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
    file: file,
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

export const validateFileBeforeUpload = (file: File): Promise<{ isValid: boolean; error?: string; warning?: string }> => {
  return new Promise((resolve) => {
    // Basic validation first
    const basicValidation = validateVideoFile(file);
    if (!basicValidation.isValid) {
      resolve(basicValidation);
      return;
    }

    // Additional checks for video file integrity
    const video = document.createElement('video');
    video.preload = 'metadata';
    
    const timeout = setTimeout(() => {
      resolve({
        isValid: false,
        error: 'File validation timed out. Please try again.',
      });
    }, 10000); // 10 second timeout

    video.onloadedmetadata = () => {
      clearTimeout(timeout);
      
      // Check if video has valid duration
      if (video.duration === Infinity || video.duration === 0) {
        resolve({
          isValid: false,
          error: 'Invalid video file. Please select a valid video.',
        });
        return;
      }

      // Check video dimensions
      if (video.videoWidth === 0 || video.videoHeight === 0) {
        resolve({
          isValid: false,
          error: 'Video file appears to be corrupted or invalid.',
        });
        return;
      }

      // Warning for very large files
      if (file.size > 100 * 1024 * 1024) { // 100MB
        resolve({
          isValid: true,
          warning: 'Large file detected. Upload may take longer than usual.',
        });
        return;
      }

      resolve({ isValid: true });
    };

    video.onerror = () => {
      clearTimeout(timeout);
      resolve({
        isValid: false,
        error: 'Could not read video file. Please ensure it\'s a valid video format.',
      });
    };

    video.src = URL.createObjectURL(file);
  });
}; 