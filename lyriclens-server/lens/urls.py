from django.urls import path
from .views.song import get_song_summary

urlpatterns = [
    path('song/summary', get_song_summary, name='get_song_summary'),
]