from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import logging
import json

from lens.services.lyrics_analysis_service import LyricsAnalysisService
from lens.services.lyricsovh_service import LyricsOvhService
# Set up logging
logger = logging.getLogger(__name__)

# Initialize services once at module level
lyrics_analysis_service = LyricsAnalysisService()
lyrics_ovh_service = LyricsOvhService()

@api_view(['GET'])
def get_suggestions(request):
    """
    API endpoint to get song suggestions based on a search query using lyrics.ovh.
    
    Query Parameters:
        query (str): Required. The search query
        
    Returns:
        JsonResponse: Song suggestions or error message
    """
    query = request.GET.get('query')
    
    # Validate required parameters
    if not query:
        return Response(
            {"error": "query parameter is required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Get suggestions from the service
        result = lyrics_ovh_service.get_suggestions(query)
        
        # Check if there was an error
        if "error" in result:
            return Response(result, status=status.HTTP_404_NOT_FOUND)
        
        # Format the response to simplify the data structure
        suggestions = []
        
        # Extract data from the response
        if "data" in result and isinstance(result["data"], list):
            for item in result["data"]:
                suggestions.append({
                    "title": item.get("title", ""),
                    "artist": item.get("artist", {}).get("name", ""),
                    "album": item.get("album", {}).get("title", ""),
                    "preview_url": item.get("preview", ""),
                    "cover_url": item.get("album", {}).get("cover_medium", "")
                })
        
        response_data = {
            "query": query,
            "suggestions": suggestions,
            "total": len(suggestions)
        }
        
        return Response(response_data)
    except Exception as e:
        logger.error(f"Unexpected error in get_suggestions view: {e}")
        return Response(
            {"error": f"An unexpected error occurred: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_lyrics(request):
    """
    API endpoint to fetch lyrics for a song using lyrics.ovh.
    
    Query Parameters:
        artist_name (str): Required. The artist name
        track_name (str): Required. The song title
        
    Returns:
        JsonResponse: Lyrics data or error message
    """
    artist = request.GET.get('artist_name')
    song = request.GET.get('track_name')
    
    # Validate required parameters
    if not artist:
        return Response(
            {"error": "artist parameter is required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not song:
        return Response(
            {"error": "song parameter is required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Get lyrics from the service
        result = lyrics_ovh_service.get_lyrics(artist, song)
        
        # Check if there was an error
        if "error" in result:
            return Response(result, status=status.HTTP_404_NOT_FOUND)
        
        # Return the lyrics
        return Response(result)
    except Exception as e:
        logger.error(f"Unexpected error in get_lyrics view: {e}")
        return Response(
            {"error": f"An unexpected error occurred: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    

@api_view(['POST'])
def analyze_lyrics(request):
    """
    API endpoint to analyze lyrics for a song.
    
    This endpoint uses DeepSeek to analyze the lyrics from MusixMatch and provides:
    1. A concise summary of what the song is about
    2. A list of countries mentioned in the lyrics (if any)
    
    Note: The analysis is based on partial lyrics provided by MusixMatch due to
    copyright restrictions.
    
    Query Parameters:
        track_name (str): Required. The name of the track to search for
        artist_name (str): Required. The artist name
        lyrics (str): Required. The lyrics to analyze
    Returns:
        JsonResponse: Analysis results or error message
    """
    track_name = request.data.get('track_name')
    artist_name = request.data.get('artist_name')
    lyrics = request.data.get('lyrics')

    # Validate required parameters
    if not track_name:
        return Response(
            {"error": "track_name parameter is required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not artist_name:
        return Response(
            {"error": "artist_name parameter is required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Use the global service instance instead of creating a new one
        result = lyrics_analysis_service.analyze_lyrics(track_name, artist_name, lyrics)
        
        # Check if there was an error
        if "error" in result:
            return Response(result, status=status.HTTP_404_NOT_FOUND)
        
        # Parse the analysis JSON to format it nicely
        try:
            analysis_json = json.loads(result["analysis"])
            
            # Create the formatted response
            response_data = {
                "track_name": result["track_name"],
                "artist_name": result["artist_name"],
                "summary": analysis_json.get("summary", "No summary available"),
                "countries_mentioned": analysis_json.get("countries_mentioned", []),
            }
            
            return Response(response_data)
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing analysis JSON: {e}")
            
            # Return the raw analysis if JSON parsing fails
            return Response(result)
            
    except Exception as e:
        logger.error(f"Unexpected error in analyze_lyrics view: {e}")
        return Response(
            {"error": f"An unexpected error occurred: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) 