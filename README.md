# VidelizerAI

An AI-powered video analysis platform that provides transcription, sentiment analysis, and key insights from uploaded videos.

## Features

- **Video Upload**: Drag and drop video files for analysis
- **AI Analysis**: Get comprehensive insights including:
  - Video transcription
  - Sentiment analysis
  - Key points extraction
  - Duration and language detection
- **Results Dashboard**: View and filter analysis results
- **Real-time Progress**: Track analysis status and progress

## Tech Stack

- **Frontend**: React 19, TypeScript, Tailwind CSS
- **Backend**: Node.js, Express (planned)
- **AI Services**: OpenAI Whisper, GPT-4 (planned)

## Live Demo

Visit the live application: [VidelizerAI on GitHub Pages](https://tishify.github.io/VidelizerAI)

## Local Development

### Prerequisites

- Node.js 18 or higher
- npm or yarn

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Tishify/VidelizerAI.git
cd VidelizerAI
```

2. Install dependencies:
```bash
cd frontend
npm install
```

3. Start the development server:
```bash
npm start
```

The application will be available at `http://localhost:3000`

### Build for Production

```bash
npm run build
```

## Deployment

### GitHub Pages (Automatic)

The application is automatically deployed to GitHub Pages when changes are pushed to the main branch. The deployment is handled by GitHub Actions.

### Manual Deployment

To manually deploy to GitHub Pages:

```bash
cd frontend
npm run deploy
```

This will:
1. Build the production version
2. Deploy to the `gh-pages` branch
3. Make the app available at `https://tishify.github.io/VidelizerAI`

## Project Structure

```
VidelizerAI/
├── frontend/                 # React application
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── types/          # TypeScript type definitions
│   ├── public/             # Static assets
│   └── package.json        # Dependencies and scripts
├── backend/                # Backend API (planned)
├── documentation/          # Project documentation
└── .github/workflows/     # GitHub Actions workflows
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Roadmap

- [ ] Backend API implementation
- [ ] Real video processing and analysis
- [ ] User authentication
- [ ] Video storage and management
- [ ] Advanced analytics dashboard
- [ ] Mobile responsive design improvements 