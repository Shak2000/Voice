# Quotes Reading App

A client-server application that generates inspiring quotes on any subject using Gemini 2.5 Flash Lite and provides text-to-speech functionality.

## Features

- **Quote Generation**: Enter any subject and get 5 inspiring quotes with context
- **Text-to-Speech**: Click the "Play" button to hear quotes read aloud
- **Modern UI**: Beautiful, responsive design with smooth animations
- **Fallback Support**: Browser TTS fallback if Gemini TTS is unavailable

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up Gemini API Key

You need a Gemini API key to use this application. Get one from [Google AI Studio](https://makersuite.google.com/app/apikey).

**Option 1: Environment Variable**
```bash
export GEMINI_API_KEY="your_api_key_here"
```

**Option 2: .env File**
```bash
cp .env.example .env
# Edit .env and add your actual API key
```

The app will automatically detect the API key from either method.

### 3. Test the Setup (Optional)

```bash
python test_setup.py
```

This will verify that all dependencies are installed and the API key is configured correctly.

### 4. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:8000`

## Project Structure

```
├── app.py              # FastAPI server with API endpoints
├── quotes.py           # Gemini integration for quote generation
├── requirements.txt    # Python dependencies
├── static/
│   ├── quotes.html     # Main HTML page
│   ├── quotes.js       # Client-side JavaScript
│   └── styles.css      # CSS styling
└── README.md          # This file
```

## API Endpoints

- `GET /` - Serves the main HTML page
- `POST /api/quotes` - Generates quotes for a given subject
- `POST /api/tts` - Converts text to speech

## Usage

1. Open your browser and go to `http://localhost:8000`
2. Enter a subject in the text box (e.g., "success", "motivation", "wisdom")
3. Click "Get Quotes" to generate quotes
4. Click the "Play" button next to any quote to hear it read aloud

## Technical Details

- **Backend**: FastAPI with Python
- **AI Model**: Gemini 2.5 Flash Lite for quote generation
- **TTS**: Gemini 2.5 Flash Preview TTS (with browser fallback)
- **Frontend**: Vanilla HTML, CSS, and JavaScript
- **Styling**: Modern gradient design with responsive layout

## Notes

- The TTS implementation includes a fallback to browser's built-in speech synthesis
- The app handles errors gracefully with user-friendly messages
- All quotes are properly escaped to prevent XSS attacks
- The design is fully responsive and works on mobile devices