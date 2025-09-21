# Quotes Reading App

A client-server application that generates inspiring quotes on any subject using Gemini 2.0 Flash Experimental and provides text-to-speech functionality with real Google Cloud Gemini TTS voices.

## Features

- **Smart Quote Generation**: Enter any subject and get 5 inspiring quotes with context
- **Person Detection**: Automatically detects if the subject is a person's name and returns quotes BY that person rather than ABOUT them
- **Real Gemini TTS**: 30 distinct voices using Google Cloud Text-to-Speech with Gemini TTS technology
- **Voice Selection**: Choose from Male/Female voices with natural characteristics
- **Settings Page**: Configure and test different voice options
- **Modern UI**: Beautiful, responsive design with smooth animations and navigation
- **Fallback Support**: Browser TTS fallback if Google Cloud authentication is not configured

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up Gemini API Key

You need a Gemini API key for quote generation. Get one from [Google AI Studio](https://makersuite.google.com/app/apikey).

The API key is already configured in `config.py`, but you can update it if needed.

### 3. Set up Google Cloud Authentication (for Real TTS)

For real Gemini TTS voices, you need Google Cloud authentication. See `SETUP_GEMINI_TTS.md` for detailed instructions.

**Quick Setup (Development)**:
```bash
# Install Google Cloud CLI, then:
gcloud auth application-default login
```

**Production Setup**:
- Create a Google Cloud service account
- Download the JSON key file
- Set environment variable:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
```

**Note**: Without Google Cloud authentication, the app will fall back to browser TTS.

### 4. Test the Setup (Optional)

```bash
python test_setup.py
```

This will verify that all dependencies are installed and the API key is configured correctly.

### 5. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:8000`

## Project Structure

```
├── app.py                  # FastAPI server with API endpoints
├── quotes.py               # Gemini integration for quote generation
├── config.py               # Configuration (API keys)
├── requirements.txt        # Python dependencies
├── SETUP_GEMINI_TTS.md     # Google Cloud TTS setup guide
├── static/
│   ├── home.html           # Home page
│   ├── home.js             # Home page JavaScript
│   ├── quotes.html         # Quotes page
│   ├── quotes.js           # Quotes page JavaScript
│   ├── settings.html       # Settings page
│   ├── settings.js         # Settings page JavaScript
│   ├── index.html          # Navigation toolbar
│   └── styles.css          # CSS styling
└── README.md              # This file
```

## API Endpoints

- `GET /` - Serves the home page
- `GET /quotes` - Serves the quotes page  
- `GET /settings` - Serves the settings page
- `POST /api/quotes` - Generates quotes for a given subject
- `POST /api/tts` - Converts text to speech using Gemini TTS
- `GET /api/voices` - Returns available Gemini TTS voices
- `POST /api/settings` - Saves voice preferences

## Usage

1. **Start the app**: Open your browser and go to `http://localhost:8000`

2. **Configure Voice (Optional)**: 
   - Go to Settings page to select your preferred voice
   - Choose from 30 Gemini TTS voices (Male/Female)
   - Test voices before saving

3. **Generate Quotes**:
   - Go to Quotes page and enter a subject:
     - **Topics**: "success", "motivation", "wisdom", "love", "happiness"
     - **People**: "Einstein", "Churchill", "Steve Jobs", "Maya Angelou", "Nelson Mandela"
   - Click "Get Quotes" to generate quotes
     - For topics: Returns quotes about the subject from various people
     - For people: Returns quotes BY that person (not about them)

4. **Listen to Quotes**:
   - Click the "Play" button next to any quote
   - Uses your selected Gemini TTS voice (or browser TTS as fallback)
   - Each voice has distinct characteristics for variety

## Technical Details

- **Backend**: FastAPI with Python
- **AI Model**: Gemini 2.0 Flash Experimental for quote generation
- **TTS**: Google Cloud Text-to-Speech with Gemini TTS technology
- **Voices**: 30 distinct voices (gemini-2.5-flash-preview-tts model)
- **Frontend**: Vanilla HTML, CSS, and JavaScript with navigation
- **Styling**: Modern gradient design with responsive layout
- **Authentication**: Google Cloud Application Default Credentials

## Voice Features

- **Real Gemini TTS**: Uses Google Cloud's advanced Gemini TTS technology
- **Voice Variety**: 30 unique voices with distinct male/female characteristics
- **Quality**: High-quality, natural-sounding speech synthesis
- **Style Control**: Advanced prompting capabilities for expression control
- **Fallback**: Graceful degradation to browser TTS if Cloud auth unavailable

## Notes

- **Authentication Required**: Real TTS requires Google Cloud authentication (see `SETUP_GEMINI_TTS.md`)
- **Fallback Behavior**: Automatically falls back to browser TTS if Google Cloud unavailable
- **Error Handling**: Graceful error handling with user-friendly messages
- **Security**: All quotes properly escaped to prevent XSS attacks
- **Responsive**: Fully responsive design that works on mobile devices
- **Navigation**: Multi-page app with persistent voice settings