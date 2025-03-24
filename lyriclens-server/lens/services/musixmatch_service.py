"""
Service for interacting with the MusixMatch API to fetch song lyrics.
"""
import os
import requests
import json
import logging
from dotenv import load_dotenv

# Set up logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class MusixMatchService:
    """
    Service class for interacting with the MusixMatch API to fetch song lyrics
    and other music metadata.
    """
    
    BASE_URL = "https://api.musixmatch.com/ws/1.1"
    
    def __init__(self):
        """Initialize the MusixMatch service with API key from environment variables."""
        self.api_key = os.getenv("MUSIXMATCH_API_KEY")
        if not self.api_key:
            logger.warning("MUSIXMATCH_API_KEY not found in environment variables")
    
    def search_tracks(self, query, page=1, page_size=10):
        """
        Search for tracks by keyword.
        
        Args:
            query (str): The search query (song name or keywords)
            page (int, optional): Page number for pagination. Defaults to 1.
            page_size (int, optional): Number of results per page. Defaults to 10.
            
        Returns:
            dict: Track search results or error information
        """
        endpoint = f"{self.BASE_URL}/track.search"
        params = {
            "apikey": self.api_key,
            "q": query,
            "page": page,
            "page_size": page_size,
            "s_track_rating": "desc",  # Sort by track rating (popularity)
            "f_has_lyrics": 1  # Only include tracks with lyrics
        }
        
        return self._make_request(endpoint, params)
        
    def get_lyrics(self, track_name, artist_name):
        """
        Get lyrics for a specific track by name and artist name.
        
        Args:
            track_name (str): The name of the track
            artist_name (str): The artist name
            
        Returns:
            dict: Lyrics data or error information
        """
        endpoint = f"{self.BASE_URL}/matcher.lyrics.get"
        params = {
            "apikey": self.api_key,
            "q_track": track_name,
            "q_artist": artist_name,
            "page_size": 10,
            "page": 1,
            "s_track_rating": "desc"
        }
        
        return self._make_request(endpoint, params)
    
    def _make_request(self, endpoint, params):
        """
        Make a request to the MusixMatch API.
        
        Args:
            endpoint (str): API endpoint to call
            params (dict): Query parameters
            
        Returns:
            dict: Response data or error information
        """
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error making request to MusixMatch API: {e}")
            return {"error": f"API request failed: {str(e)}"} 