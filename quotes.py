import google.generativeai as genai
import json
from typing import List, Dict

class QuotesGenerator:
    def __init__(self, api_key: str):
        # Initialize Gemini with provided API key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def generate_quotes(self, subject: str) -> List[Dict[str, str]]:
        """
        Generate quotes for a given subject using Gemini 2.5 Flash Lite
        Returns a list of dictionaries with 'quote' and 'context' keys
        """
        prompt = f"""
        Generate 5 inspiring and meaningful quotes about "{subject}". 
        For each quote, provide:
        1. The quote itself (should be impactful and memorable)
        2. Context about the quote (who said it, when, or what situation it relates to)
        
        Return the response as a JSON array where each item has this structure:
        {{
            "quote": "The actual quote text",
            "context": "Context about the quote"
        }}
        
        Make sure the quotes are diverse, inspiring, and directly related to the subject "{subject}".
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean up the response to extract JSON
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            # Parse JSON response
            quotes_data = json.loads(response_text)
            
            # Validate the structure
            if not isinstance(quotes_data, list):
                raise ValueError("Response is not a list")
            
            for item in quotes_data:
                if not isinstance(item, dict) or 'quote' not in item or 'context' not in item:
                    raise ValueError("Invalid quote structure")
            
            return quotes_data
            
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print(f"Response text: {response_text}")
            return self._get_fallback_quotes(subject)
        except Exception as e:
            print(f"Error generating quotes: {e}")
            return self._get_fallback_quotes(subject)
    
    def _get_fallback_quotes(self, subject: str) -> List[Dict[str, str]]:
        """
        Fallback quotes if Gemini API fails
        """
        fallback_quotes = {
            "success": [
                {"quote": "Success is not final, failure is not fatal: it is the courage to continue that counts.", "context": "Winston Churchill"},
                {"quote": "The way to get started is to quit talking and begin doing.", "context": "Walt Disney"},
                {"quote": "Don't be afraid to give up the good to go for the great.", "context": "John D. Rockefeller"}
            ],
            "motivation": [
                {"quote": "The only way to do great work is to love what you do.", "context": "Steve Jobs"},
                {"quote": "If you can dream it, you can do it.", "context": "Walt Disney"},
                {"quote": "The future belongs to those who believe in the beauty of their dreams.", "context": "Eleanor Roosevelt"}
            ],
            "life": [
                {"quote": "Life is what happens to you while you're busy making other plans.", "context": "John Lennon"},
                {"quote": "The purpose of our lives is to be happy.", "context": "Dalai Lama"},
                {"quote": "Get busy living or get busy dying.", "context": "Stephen King"}
            ]
        }
        
        # Return quotes based on subject or default to success quotes
        subject_lower = subject.lower()
        for key in fallback_quotes:
            if key in subject_lower:
                return fallback_quotes[key]
        
        return fallback_quotes["success"]