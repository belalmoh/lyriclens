from django.urls import path
from .views.song import get_lyrics, analyze_lyrics, get_suggestions

urlpatterns = [
    path('song/search', get_suggestions, name='search_songs'),
    path('song/lyrics', get_lyrics, name='get_lyrics'),
    path('song/analyze', analyze_lyrics, name='analyze_lyrics'),
]