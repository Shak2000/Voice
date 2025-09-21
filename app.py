from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from quotes import QuotesGenerator
import google.generativeai as genai
from google.cloud import texttospeech
import tempfile
import base64
from typing import List, Dict
import config
import os

app = FastAPI(title="Quotes Reading App")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize quotes generator (will be created on first use)
quotes_generator = None

def get_quotes_generator():
    """Get or create the quotes generator instance"""
    global quotes_generator
    if quotes_generator is None:
        quotes_generator = QuotesGenerator(config.GEMINI_API_KEY)
    return quotes_generator

class QuoteRequest(BaseModel):
    subject: str

class QuoteResponse(BaseModel):
    quotes: List[Dict[str, str]]
    is_person: bool

class TTSRequest(BaseModel):
    text: str
    voice_id: str = "Aoede"  # Default voice
    model_name: str = "gemini-2.5-flash-preview-tts"  # Default model
    prompt: str = ""  # Optional style prompt

class TTSResponse(BaseModel):
    audio_data: str  # Base64 encoded audio

class VoiceOption(BaseModel):
    id: str
    name: str
    description: str
    gender: str

class VoicesResponse(BaseModel):
    voices: List[VoiceOption]

class SettingsRequest(BaseModel):
    voice_id: str

class SettingsResponse(BaseModel):
    success: bool
    message: str

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the home page"""
    return FileResponse("static/home.html")

@app.get("/quotes", response_class=HTMLResponse)
async def read_quotes():
    """Serve the quotes page"""
    return FileResponse("static/quotes.html")

@app.get("/settings", response_class=HTMLResponse)
async def read_settings():
    """Serve the settings page"""
    return FileResponse("static/settings.html")

@app.post("/api/quotes", response_model=QuoteResponse)
async def get_quotes(request: QuoteRequest):
    """
    Generate quotes for a given subject using Gemini 2.5 Flash Lite
    """
    try:
        if not request.subject.strip():
            raise HTTPException(status_code=400, detail="Subject cannot be empty")
        
        generator = get_quotes_generator()
        result = generator.generate_quotes(request.subject.strip())
        return QuoteResponse(quotes=result["quotes"], is_person=result["is_person"])
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating quotes: {str(e)}")

@app.post("/api/tts", response_model=TTSResponse)
async def text_to_speech(request: TTSRequest):
    """
    Convert text to speech using Gemini 2.5 Flash Preview TTS
    """
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        # Configure Gemini for TTS
        genai.configure(api_key=config.GEMINI_API_KEY)
        
        # Generate speech using Gemini TTS with selected voice
        audio_data = await generate_speech_with_gemini(
            text=request.text, 
            voice_id=request.voice_id,
            model_name=request.model_name,
            prompt=request.prompt
        )
        
        return TTSResponse(audio_data=audio_data)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating speech: {str(e)}")

async def generate_speech_with_gemini(text: str, voice_id: str = "Aoede", model_name: str = "gemini-2.5-flash-preview-tts", prompt: str = "") -> str:
    """
    Generate speech using Gemini TTS with specified voice via Google Cloud Text-to-Speech API
    """
    try:
        # Log the voice selection for debugging
        print(f"Attempting Gemini TTS with voice: {voice_id}, model: {model_name} for text: '{text[:50]}...'")
        
        # Initialize Google Cloud Text-to-Speech client
        client = texttospeech.TextToSpeechClient()
        
        # Create synthesis input with optional prompt
        synthesis_input = texttospeech.SynthesisInput(
            text=text,
            prompt=prompt if prompt else f"Say the following in a natural, clear voice"
        )
        
        # Select the voice
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name=voice_id,
            model_name=model_name
        )
        
        # Configure audio output
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        
        # Perform the text-to-speech request
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice, 
            audio_config=audio_config
        )
        
        # Encode audio as base64 data URL
        audio_base64 = base64.b64encode(response.audio_content).decode('utf-8')
        audio_data_url = f"data:audio/mp3;base64,{audio_base64}"
        
        print(f"Successfully generated speech with Gemini TTS voice: {voice_id}")
        return audio_data_url
        
    except Exception as e:
        print(f"Gemini TTS error: {e}")
        print(f"Falling back to browser TTS with voice preference: {voice_id}")
        return "USE_BROWSER_TTS"

@app.get("/api/voices", response_model=VoicesResponse)
async def get_available_voices():
    """
    Get available voices for Gemini TTS (based on official Google Cloud documentation)
    """
    # Official Gemini TTS voices from Google Cloud documentation with correct gender mapping
    voices = [
        VoiceOption(id="Achernar", name="Achernar", description="Gemini TTS Voice - US English", gender="Female"),
        VoiceOption(id="Achird", name="Achird", description="Gemini TTS Voice - US English", gender="Male"),
        VoiceOption(id="Algenib", name="Algenib", description="Gemini TTS Voice - US English", gender="Male"),
        VoiceOption(id="Algieba", name="Algieba", description="Gemini TTS Voice - US English", gender="Male"),
        VoiceOption(id="Alnilam", name="Alnilam", description="Gemini TTS Voice - US English", gender="Male"),
        VoiceOption(id="Aoede", name="Aoede", description="Gemini TTS Voice - US English (Default)", gender="Female"),
        VoiceOption(id="Autonoe", name="Autonoe", description="Gemini TTS Voice - US English", gender="Female"),
        VoiceOption(id="Callirrhoe", name="Callirrhoe", description="Gemini TTS Voice - US English", gender="Female"),
        VoiceOption(id="Charon", name="Charon", description="Gemini TTS Voice - US English", gender="Male"),
        VoiceOption(id="Despina", name="Despina", description="Gemini TTS Voice - US English", gender="Female"),
        VoiceOption(id="Enceladus", name="Enceladus", description="Gemini TTS Voice - US English", gender="Male"),
        VoiceOption(id="Erinome", name="Erinome", description="Gemini TTS Voice - US English", gender="Female"),
        VoiceOption(id="Fenrir", name="Fenrir", description="Gemini TTS Voice - US English", gender="Male"),
        VoiceOption(id="Gacrux", name="Gacrux", description="Gemini TTS Voice - US English", gender="Female"),
        VoiceOption(id="Iapetus", name="Iapetus", description="Gemini TTS Voice - US English", gender="Male"),
        VoiceOption(id="Kore", name="Kore", description="Gemini TTS Voice - US English", gender="Female"),
        VoiceOption(id="Laomedeia", name="Laomedeia", description="Gemini TTS Voice - US English", gender="Female"),
        VoiceOption(id="Leda", name="Leda", description="Gemini TTS Voice - US English", gender="Female"),
        VoiceOption(id="Orus", name="Orus", description="Gemini TTS Voice - US English", gender="Male"),
        VoiceOption(id="Pulcherrima", name="Pulcherrima", description="Gemini TTS Voice - US English", gender="Female"),
        VoiceOption(id="Puck", name="Puck", description="Gemini TTS Voice - US English", gender="Male"),
        VoiceOption(id="Rasalgethi", name="Rasalgethi", description="Gemini TTS Voice - US English", gender="Male"),
        VoiceOption(id="Sadachbia", name="Sadachbia", description="Gemini TTS Voice - US English", gender="Male"),
        VoiceOption(id="Sadaltager", name="Sadaltager", description="Gemini TTS Voice - US English", gender="Male"),
        VoiceOption(id="Schedar", name="Schedar", description="Gemini TTS Voice - US English", gender="Male"),
        VoiceOption(id="Sulafat", name="Sulafat", description="Gemini TTS Voice - US English", gender="Female"),
        VoiceOption(id="Umbriel", name="Umbriel", description="Gemini TTS Voice - US English", gender="Male"),
        VoiceOption(id="Vindemiatrix", name="Vindemiatrix", description="Gemini TTS Voice - US English", gender="Female"),
        VoiceOption(id="Zephyr", name="Zephyr", description="Gemini TTS Voice - US English", gender="Female"),
        VoiceOption(id="Zubenelgenubi", name="Zubenelgenubi", description="Gemini TTS Voice - US English", gender="Male"),
    ]
    
    return VoicesResponse(voices=voices)

@app.post("/api/settings", response_model=SettingsResponse)
async def save_settings(request: SettingsRequest):
    """
    Save user settings (voice preference)
    """
    try:
        # In a real application, you would save this to a database or config file
        # For now, we'll just validate the voice exists
        voices_response = await get_available_voices()
        voice_ids = [voice.id for voice in voices_response.voices]
        
        if request.voice_id not in voice_ids:
            raise HTTPException(status_code=400, detail="Invalid voice ID")
        
        # Here you would typically save to database or session
        # For demo purposes, we'll just return success
        return SettingsResponse(success=True, message=f"Voice setting saved: {request.voice_id}")
    
    except Exception as e:
        return SettingsResponse(success=False, message=f"Error saving settings: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)