export interface VideoFile {
  id: string;
  name: string;
  size: number;
  type: string;
  lastModified: number;
  preview?: string;
}

export interface AnalysisResult {
  id: string;
  videoId: string;
  status: 'pending' | 'processing' | 'completed' | 'error';
  progress?: number;
  result?: {
    summary: string;
    keyPoints: string[];
    sentiment: 'positive' | 'negative' | 'neutral';
    duration: number;
    language?: string;
  };
  error?: string;
  createdAt: Date;
  completedAt?: Date;
}

export interface UploadResponse {
  success: boolean;
  videoId?: string;
  error?: string;
}

export interface AnalysisRequest {
  videoId: string;
  options?: {
    language?: string;
    includeTranscript?: boolean;
    includeSentiment?: boolean;
  };
} 