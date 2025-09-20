from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from quotes import QuotesGenerator
import google.generativeai as genai
import tempfile
import base64
from typing import List, Dict
import config

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

class TTSRequest(BaseModel):
    text: str

class TTSResponse(BaseModel):
    audio_data: str  # Base64 encoded audio

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page"""
    return FileResponse("static/quotes.html")

@app.post("/api/quotes", response_model=QuoteResponse)
async def get_quotes(request: QuoteRequest):
    """
    Generate quotes for a given subject using Gemini 2.5 Flash Lite
    """
    try:
        if not request.subject.strip():
            raise HTTPException(status_code=400, detail="Subject cannot be empty")
        
        generator = get_quotes_generator()
        quotes = generator.generate_quotes(request.subject.strip())
        return QuoteResponse(quotes=quotes)
    
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
        
        # Generate speech using Gemini TTS
        # Note: This is a simplified implementation. In practice, you might need to use
        # a different TTS service or the actual Gemini TTS API when it becomes available
        audio_data = await generate_speech_with_gemini(request.text)
        
        return TTSResponse(audio_data=audio_data)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating speech: {str(e)}")

async def generate_speech_with_gemini(text: str) -> str:
    """
    Generate speech using Gemini 2.5 Flash Preview TTS
    """
    try:
        # Use Gemini's generative model for TTS
        # The model can generate audio content
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Create a prompt for TTS
        prompt = f"Convert this text to speech: {text}"
        
        # Generate the response
        response = model.generate_content(prompt)
        
        # Check if the response contains audio data
        if hasattr(response, 'parts') and response.parts:
            for part in response.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    # Convert to base64 data URL
                    import base64
                    audio_base64 = base64.b64encode(part.inline_data.data).decode('utf-8')
                    return f"data:audio/wav;base64,{audio_base64}"
        
        # If no audio data found, fall back to browser TTS
        return "USE_BROWSER_TTS"
        
    except Exception as e:
        # Fallback: return a signal that browser TTS should be used
        return "USE_BROWSER_TTS"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)