# Gemini TTS Setup Instructions

This application now uses real Google Cloud Gemini TTS instead of browser fallback. To enable this functionality, you need to set up Google Cloud authentication.

## Prerequisites

1. **Google Cloud Project**: Create or use an existing Google Cloud project
2. **Enable APIs**: Enable the Text-to-Speech API in your project
3. **Authentication**: Set up authentication credentials

## Setup Steps

### Option 1: Service Account Key (Recommended for Production)

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. Navigate to "IAM & Admin" → "Service Accounts"
4. Create a new service account or select an existing one
5. Create a key for the service account (JSON format)
6. Download the key file to your local machine
7. Set the environment variable:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
   ```

### Option 2: Application Default Credentials (for Development)

1. Install the Google Cloud CLI (gcloud)
2. Run the following command:
   ```bash
   gcloud auth application-default login
   ```
3. Follow the browser authentication flow

### Option 3: For Google Compute Engine

If running on Google Compute Engine, the credentials are automatically available through the metadata server.

## Voice Information

The app now uses the official Gemini TTS voices from Google Cloud:

- **Models Available**: `gemini-2.5-flash-preview-tts` (default), `gemini-2.5-pro-preview-tts`
- **Languages**: English (US) only in preview
- **Voices**: 30 unique voices with distinct characteristics (Male/Female)
- **Advanced Features**: Style control via prompts, dynamic performance, enhanced pace control

## Testing

Once authentication is set up, different voice selections will produce genuinely different audio using Google's Gemini TTS technology instead of browser fallback.

## Fallback Behavior

If Google Cloud authentication fails, the app will gracefully fall back to browser TTS with a message in the console logs.

## References

- [Official Gemini TTS Documentation](https://cloud.google.com/text-to-speech/docs/gemini-tts)
- [Google Cloud Authentication Guide](https://cloud.google.com/docs/authentication)
