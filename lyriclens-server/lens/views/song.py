from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import logging
import json

from lens.services.musixmatch_service import MusixMatchService
from lens.services.lyrics_analysis_service import LyricsAnalysisService

# Set up logging
logger = logging.getLogger(__name__)

# Initialize services once at module level
musixmatch_service = MusixMatchService()
lyrics_analysis_service = LyricsAnalysisService()

@api_view(['GET'])
def search_songs(request):
    """
    API endpoint to search for songs by keyword.
    
    Query Parameters:
        query (str): Required. The search term to find songs
        page (int): Optional. Page number for pagination (default: 1)
        page_size (int): Optional. Number of results per page (default: 10)
        
    Returns:
        JsonResponse: List of matching songs with metadata
    """
    query = request.GET.get('query')
    page = request.GET.get('page', '1')
    page_size = request.GET.get('page_size', '10')
    
    # Validate required parameters
    if not query:
        return Response(
            {"error": "query parameter is required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Validate and convert pagination parameters
    try:
        page = int(page)
        page_size = int(page_size)
        
        # Limit page_size to reasonable values
        if page_size > 50:
            page_size = 50
        elif page_size < 1:
            page_size = 10
            
        if page < 1:
            page = 1
            
    except ValueError:
        return Response(
            {"error": "page and page_size must be valid integers"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Use the global service instance to search for tracks
        result = musixmatch_service.search_tracks(query, page, page_size)
        
        # Check if there was an error
        if "error" in result:
            return Response(result, status=status.HTTP_404_NOT_FOUND)
        
        # Extract the track list from the response
        try:
            message = result.get("message", {})
            header = message.get("header", {})
            body = message.get("body", {})
            track_list = body.get("track_list", [])
            
            # Format the response with relevant track information
            songs = []
            for track_item in track_list:
                track = track_item.get("track", {})
                songs.append({
                    "track_id": track.get("track_id"),
                    "track_name": track.get("track_name"),
                    "artist_name": track.get("artist_name"),
                    "album_name": track.get("album_name"),
                })
            
            # Build the complete response with pagination info
            response_data = {
                "songs": songs,
                "pagination": {
                    "current_page": page,
                    "page_size": page_size,
                    "total_results": header.get("available", 0)
                },
                "status_code": header.get("status_code")
            }
            
            return Response(response_data)
        except (KeyError, TypeError) as e:
            logger.error(f"Error parsing search response: {e}")
            return Response(
                {"error": "Could not parse search results from the API response"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    except Exception as e:
        logger.error(f"Unexpected error in search_songs view: {e}")
        return Response(
            {"error": f"An unexpected error occurred: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_lyrics(request):
    """
    API endpoint to fetch lyrics for a song.
    
    Query Parameters:
        track_name (str): Required. The name of the track to search for
        artist_name (str): Optional. The artist name to filter results
        
    Returns:
        JsonResponse: Lyrics data or error message
    """
    track_name = request.GET.get('track_name')
    artist_name = request.GET.get('artist_name')
    
    if not track_name:
        return Response(
            {"error": "track_name parameter is required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Use the global service instance instead of creating a new one
        result = musixmatch_service.get_lyrics(track_name, artist_name)
        
        # Check if there was an error
        if "error" in result:
            return Response(result, status=status.HTTP_404_NOT_FOUND)
        
        # Extract the lyrics data from the response
        try:
            lyrics_body = result.get("message", {}).get("body", {}).get("lyrics", {}).get("lyrics_body", "")
            lyrics_copyright = result.get("message", {}).get("body", {}).get("lyrics", {}).get("lyrics_copyright", "")
            
            response_data = {
                "lyrics": lyrics_body,
                "copyright": lyrics_copyright
            }
            
            return Response(response_data)
        except (KeyError, TypeError) as e:
            logger.error(f"Error parsing lyrics response: {e}")
            return Response(
                {"error": "Could not parse lyrics from the API response"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    except Exception as e:
        logger.error(f"Unexpected error in get_lyrics view: {e}")
        return Response(
            {"error": f"An unexpected error occurred: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    

@api_view(['GET'])
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
        
    Returns:
        JsonResponse: Analysis results or error message
    """
    track_name = request.GET.get('track_name')
    artist_name = request.GET.get('artist_name')
    
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
        result = lyrics_analysis_service.analyze_lyrics(track_name, artist_name)
        
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
                "disclaimer": result["disclaimer"]
            }
            
            # Add a message if no countries are mentioned
            if not response_data["countries_mentioned"]:
                response_data["countries_message"] = "No countries mentioned in the lyrics"
            else:
                response_data["countries_message"] = f"Countries mentioned: {', '.join(response_data['countries_mentioned'])}"
            
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