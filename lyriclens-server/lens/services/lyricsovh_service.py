"""
Service for interacting with the lyrics.ovh API to fetch song lyrics and suggestions.
"""
import requests
import logging

# Set up logging
logger = logging.getLogger(__name__)

class LyricsOvhService:
    """
    Service class for interacting with the lyrics.ovh API.
    
    This service provides methods to:
    1. Get lyrics for a specific artist and song
    2. Get suggestions based on a search query
    """
    
    BASE_URL = "https://api.lyrics.ovh/v1"
    SUGGEST_URL = "https://api.lyrics.ovh/suggest"
    
    def __init__(self):
        """Initialize the lyrics.ovh service."""
        logger.info("LyricsOvh service initialized")
    
    def get_lyrics(self, artist, song):
        """
        Get lyrics for a specific artist and song.
        
        Args:
            artist (str): The artist name
            song (str): The song title
            
        Returns:
            dict: Lyrics data or error information
        """
        try:
            # Format the URL with artist and song
            url = f"{self.BASE_URL}/{artist}/{song}"
            
            # Make the request
            response = requests.get(url)
            response.raise_for_status()
            
            # Return the JSON response
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching lyrics from lyrics.ovh: {e}")
            return {"error": f"Failed to fetch lyrics: {str(e)}"}
    
    def get_suggestions(self, query):
        """
        Get song suggestions based on a search query.
        
        Args:
            query (str): The search query
            
        Returns:
            dict: Song suggestions or error information
        """
        try:
            # Format the URL with the query
            url = f"{self.SUGGEST_URL}/{query}"
            
            # Make the request
            response = requests.get(url)
            response.raise_for_status()
            
            # Return the JSON response
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching suggestions from lyrics.ovh: {e}")
            return {"error": f"Failed to fetch suggestions: {str(e)}"} 