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
        # First, determine if the subject is a person's name
        person_check_prompt = f"""
        Determine if "{subject}" is the name of a person (famous person, historical figure, celebrity, author, etc.).
        Respond with only "YES" if it's a person's name, or "NO" if it's not a person's name.
        """
        
        try:
            person_response = self.model.generate_content(person_check_prompt)
            is_person = person_response.text.strip().upper() == "YES"
        except Exception:
            # If we can't determine, assume it's not a person
            is_person = False
        
        if is_person:
            prompt = f"""
            Generate 5 inspiring and meaningful quotes BY "{subject}" (quotes that this person actually said or wrote).
            For each quote, provide:
            1. The quote itself (should be impactful and memorable)
            2. Context about when/where the quote was said or what situation it relates to
            
            Return the response as a JSON array where each item has this structure:
            {{
                "quote": "The actual quote text",
                "context": "Context about when/where the quote was said"
            }}
            
            Make sure all quotes are actually attributed to "{subject}" and are authentic quotes by this person.
            """
        else:
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
            
            Make sure the quotes are diverse, inspiring, and directly related to the subject "{subject} and that they were actually spoken by someone and/or written in a document.".
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
        # Check if subject might be a person's name (simple heuristic)
        subject_lower = subject.lower()
        
        # Common person names that might be searched
        person_quotes = {
            "einstein": [
                {"quote": "Imagination is more important than knowledge.", "context": "Albert Einstein"},
                {"quote": "The important thing is not to stop questioning.", "context": "Albert Einstein"},
                {"quote": "Try not to become a person of success, but rather try to become a person of value.", "context": "Albert Einstein"}
            ],
            "churchill": [
                {"quote": "Success is not final, failure is not fatal: it is the courage to continue that counts.", "context": "Winston Churchill"},
                {"quote": "We shall never surrender.", "context": "Winston Churchill"},
                {"quote": "If you're going through hell, keep going.", "context": "Winston Churchill"}
            ],
            "jobs": [
                {"quote": "The only way to do great work is to love what you do.", "context": "Steve Jobs"},
                {"quote": "Stay hungry, stay foolish.", "context": "Steve Jobs"},
                {"quote": "Innovation distinguishes between a leader and a follower.", "context": "Steve Jobs"}
            ],
            "disney": [
                {"quote": "If you can dream it, you can do it.", "context": "Walt Disney"},
                {"quote": "The way to get started is to quit talking and begin doing.", "context": "Walt Disney"},
                {"quote": "All our dreams can come true, if we have the courage to pursue them.", "context": "Walt Disney"}
            ]
        }
        
        # Check if subject matches any person names
        for person_name in person_quotes:
            if person_name in subject_lower:
                return person_quotes[person_name]
        
        # General topic quotes
        topic_quotes = {
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
        for key in topic_quotes:
            if key in subject_lower:
                return topic_quotes[key]
        
        return topic_quotes["success"]