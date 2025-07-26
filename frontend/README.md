# VidelizerAI Frontend

A React TypeScript application for video analysis with AI-powered insights.

## Features

- **Drag & Drop Video Upload**: Easy video file upload with drag and drop functionality
- **Video Preview**: Automatic video thumbnail generation
- **File Validation**: Support for multiple video formats with size limits
- **Analysis Results**: Comprehensive display of video analysis results
- **Real-time Status**: Live updates on analysis progress
- **Search & Filter**: Advanced filtering and search capabilities
- **Modern UI**: Beautiful, responsive design with Tailwind CSS

## Tech Stack

- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **react-dropzone** for file uploads
- **axios** for API communication
- **Modern ES6+** features

## Project Structure

```
src/
├── components/
│   ├── VideoUpload/          # Drag & Drop upload component
│   ├── AnalysisResults/      # Results display component
│   └── LoadingSpinner/       # Loading indicator component
├── pages/
│   ├── UploadPage.tsx        # Main upload page
│   └── ResultsPage.tsx       # Results display page
├── services/
│   ├── api.ts               # API client service
│   └── fileUpload.ts        # File upload utilities
└── types/
    └── index.ts             # TypeScript type definitions
```

## Getting Started

### Prerequisites

- Node.js 16+ 
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

3. Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

### Available Scripts

- `npm start` - Runs the app in development mode
- `npm test` - Launches the test runner
- `npm run build` - Builds the app for production
- `npm run eject` - Ejects from Create React App (one-way operation)

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
REACT_APP_API_URL=http://localhost:8000
```

### API Configuration

The app is configured to communicate with a backend API. Update the API base URL in `src/services/api.ts` or use environment variables.

## Features in Detail

### Video Upload
- Supports MP4, AVI, MOV, WMV, FLV, WebM formats
- Maximum file size: 500MB
- Automatic video preview generation
- Real-time upload progress

### Analysis Results
- Summary generation
- Key points extraction
- Sentiment analysis
- Duration tracking
- Language detection
- Status tracking (pending, processing, completed, error)

### UI Components
- Responsive design
- Loading states
- Error handling
- Success notifications
- Search and filtering
- Status indicators

## Development

### Adding New Components

1. Create a new folder in `src/components/`
2. Create the component file with TypeScript
3. Export the component as default
4. Import and use in pages

### Styling

The project uses Tailwind CSS for styling. All components use utility classes for consistent design.

### TypeScript

All components and functions are typed with TypeScript interfaces defined in `src/types/index.ts`.

## Contributing

1. Follow the existing code structure
2. Use TypeScript for all new code
3. Add proper error handling
4. Test components thoroughly
5. Follow the established naming conventions

## License

This project is part of the VidelizerAI application.
