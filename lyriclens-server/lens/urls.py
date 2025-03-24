from django.urls import path
from .views.song import get_lyrics, analyze_lyrics, search_songs

urlpatterns = [
    path('song/lyrics', get_lyrics, name='get_lyrics'),
    path('song/analyze', analyze_lyrics, name='analyze_lyrics'),
    path('song/search', search_songs, name='search_songs'),
]