"""
Service for analyzing song lyrics using AI models (OpenAI or DeepSeek) to provide summaries and extract information.
With fallback capabilities for when APIs are unavailable or quota is exceeded.
"""
import os
import logging
import requests
from dotenv import load_dotenv

from .musixmatch_service import MusixMatchService

# Set up logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class LyricsAnalysisService:
    """
    Service for analyzing song lyrics using AI (OpenAI or DeepSeek).
    
    This service retrieves lyrics using the MusixMatch service and then
    uses an AI model to generate a summary and extract information such as
    mentioned countries from the lyrics.
    
    Includes fallback functionality when AI APIs are unavailable.
    """
    
    # Initialize DeepSeek 
    def __init__(self):
        self.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
        self.deepseek_api_url = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions")
            
        if not self.deepseek_api_key:
            logger.warning("DEEPSEEK_API_KEY not found in environment variables, using fallback")
        
        # Initialize MusixMatch service for lyrics retrieval
        self.musixmatch_service = MusixMatchService()
        
        logger.info("Lyrics analysis service initialized")
        
    def analyze_lyrics(self, track_name, artist_name):
        """
        Analyze lyrics for a specific track and artist.
        
        Steps:
        1. Retrieve lyrics using MusixMatch service
        2. Pass lyrics to AI model for analysis (or use fallback)
        3. Return summary and extracted information
        
        Args:
            track_name (str): The name of the track
            artist_name (str): The artist name
            
        Returns:
            dict: Analysis results including summary and mentioned countries
        """
        # Get lyrics from MusixMatch
        lyrics_response = self.musixmatch_service.get_lyrics(track_name, artist_name)
        
        # Check if there was an error getting lyrics
        if "error" in lyrics_response:
            return {
                "error": lyrics_response["error"],
                "track_name": track_name,
                "artist_name": artist_name
            }
        
        # Extract lyrics from the response
        try:
            lyrics_body = lyrics_response.get("message", {}).get("body", {}).get("lyrics", {}).get("lyrics_body", "")
            
            # If lyrics are empty, return an error
            if not lyrics_body:
                return {
                    "error": "No lyrics found for this track",
                    "track_name": track_name,
                    "artist_name": artist_name
                }
            
            try:
                return self._analyze_with_deepseek(track_name, artist_name, lyrics_body, lyrics_response)
            except Exception as e:
                logger.error(f"Error using DeepSeek API: {e}")
                return {
                    "error": f"Error analyzing lyrics: {str(e)}",
                    "track_name": track_name,
                    "artist_name": artist_name
                }
            
                
        except Exception as e:
            logger.error(f"Error analyzing lyrics: {e}")
            return {
                "error": f"Error analyzing lyrics: {str(e)}",
                "track_name": track_name,
                "artist_name": artist_name
            }
    
    def _analyze_with_deepseek(self, track_name, artist_name, lyrics_body, lyrics_response):
        """
        Analyze lyrics using the DeepSeek API.
        
        Args:
            track_name (str): The name of the track
            artist_name (str): The artist name
            lyrics_body (str): The lyrics to analyze
            lyrics_response (dict): The original MusixMatch response
            
        Returns:
            dict: Analysis results from DeepSeek
        """
        # Prepare the prompt for DeepSeek
        prompt = f"""
        Analyze the following song lyrics for '{track_name}' by '{artist_name}':
        
        {lyrics_body}
        
        Please provide:
        1. A concise one-paragraph summary of what the song is about. Capture the main themes and emotional tone without directly quoting large portions of the lyrics.
        2. A list of any countries mentioned in the lyrics.
        
        Format your response as JSON with the following structure:
        {{
            "summary": "your one-paragraph summary here",
            "countries_mentioned": ["Country1", "Country2"] or [] if no countries are mentioned
        }}
        
        If no countries are mentioned, return an empty array for countries_mentioned, not a string.
        """
        
        # Headers for the API request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.deepseek_api_key}"
        }
        
        # Data for the API request
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that analyzes song lyrics to provide summaries and extract information. Respond in valid JSON format."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"}
        }
        
        # Make the API request
        response = requests.post(
            self.deepseek_api_url,
            headers=headers,
            json=data
        )
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Parse the response
        response_json = response.json()
        analysis_text = response_json.get("choices", [{}])[0].get("message", {}).get("content", "{}")
        
        # Create the response with additional data
        response_data = {
            "track_name": track_name,
            "artist_name": artist_name,
            "analysis": analysis_text,
            "partial_lyrics_note": lyrics_response.get("partial_lyrics_note", ""),
            "disclaimer": "This analysis is based on partial lyrics provided by the MusixMatch API due to copyright restrictions."
        }
        
        return response_data
    
    def get_lyrics_summary(self, track_name, artist_name):
        """
        Get a summary of lyrics for a specific track and artist.
        
        This is a convenient method that returns only the summary part
        of the analysis.
        
        Args:
            track_name (str): The name of the track
            artist_name (str): The artist name
            
        Returns:
            dict: Summary of the lyrics
        """
        analysis = self.analyze_lyrics(track_name, artist_name)
        
        # If there was an error, return it
        if "error" in analysis:
            return analysis
            
        return analysis 