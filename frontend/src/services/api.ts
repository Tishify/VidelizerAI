import axios from 'axios';
import { UploadResponse, AnalysisResult, AnalysisRequest } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8080';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth token if needed
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export const videoApi = {
  // Upload video file
  uploadVideo: async (file: File): Promise<UploadResponse> => {
    const formData = new FormData();
    formData.append('video', file);
    
    const response = await api.post('/api/videos/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Start video analysis
  startAnalysis: async (request: AnalysisRequest): Promise<AnalysisResult> => {
    const response = await api.post('/api/videos/analyze', request);
    return response.data;
  },

  // Get analysis status
  getAnalysisStatus: async (analysisId: string): Promise<AnalysisResult> => {
    const response = await api.get(`/api/analysis/${analysisId}`);
    return response.data;
  },

  // Get analysis results
  getAnalysisResults: async (videoId: string): Promise<AnalysisResult[]> => {
    const response = await api.get(`/api/videos/${videoId}/analysis`);
    return response.data;
  },
};

export default api; 