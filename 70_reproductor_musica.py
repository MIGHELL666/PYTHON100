import os
import json
import random
import time
from datetime import datetime, timedelta
import threading

# Nota: Para un reproductor real necesitarías librerías como pygame, vlc-python, o similar
# Este es un simulador que muestra la funcionalidad

class MusicPlayer:
    def __init__(self):
        self.playlist = []
        self.current_song_index = 0
        self.is_playing = False
        self.is_paused = False
        self.volume = 70
        self.repeat_mode = "none"  # none, one, all
        self.shuffle_mode = False
        self.position = 0  # Posición en segundos
        self.duration = 0  # Duración total en segundos
        self.library = self.load_library()
        self.playlists = self.load_playlists()
        self.history = []
        self.favorites = self.load_favorites()
        self.equalizer = {
            "bass": 0,
            "mid": 0,
            "treble": 0,
            "preset": "normal"
        }
        
        # Hilo para simular reproducción
        self.playback_thread = None
        self.stop_playback = False
    
    def load_library(self):
        """Cargar biblioteca de música"""
        try:
            if os.path.exists('music_library.json'):
                with open('music_library.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Crear biblioteca de ejemplo
                sample_library = [
                    {
                        "id": 1,
                        "title": "Bohemian Rhapsody",
                        "artist": "Queen",
                        "album": "A Night at the Opera",
                        "duration": 355,  # 5:55
                        "genre": "Rock",
                        "year": 1975,
                        "file_path": "/music/queen/bohemian_rhapsody.mp3",
                        "play_count": 0,
                        "last_played": None
                    },
                    {
                        "id": 2,
                        "title": "Imagine",
                        "artist": "John Lennon",
                        "album": "Imagine",
                        "duration": 183,  # 3:03
                        "genre": "Rock",
                        "year": 1971,
                        "file_path": "/music/lennon/imagine.mp3",
                        "play_count": 0,
                        "last_played": None
                    },
                    {
                        "id": 3,
                        "title": "Hotel California",
                        "artist": "Eagles",
                        "album": "Hotel California",
                        "duration": 391,  # 6:31
                        "genre": "Rock",
                        "year": 1976,
                        "file_path": "/music/eagles/hotel_california.mp3",
                        "play_count": 0,
                        "last_played": None
                    },
                    {
                        "id": 4,
                        "title": "Billie Jean",
                        "artist": "Michael Jackson",
                        "album": "Thriller",
                        "duration": 294,  # 4:54
                        "genre": "Pop",
                        "year": 1982,
                        "file_path": "/music/jackson/billie_jean.mp3",
                        "play_count": 0,
                        "last_played": None
                    },
                    {
                        "id": 5,
                        "title": "Stairway to Heaven",
                        "artist": "Led Zeppelin",
                        "album": "Led Zeppelin IV",
                        "duration": 482,  # 8:02
                        "genre": "Rock",
                        "year": 1971,
                        "file_path": "/music/zeppelin/stairway_to_heaven.mp3",
                        "play_count": 0,
                        "last_played": None
                    }
                ]
                self.save_library(sample_library)
                return sample_library
        except Exception as e:
            print(f"Error cargando biblioteca: {e}")
            return []
    
    def save_library(self, library=None):
        """Guardar biblioteca de música"""
        try:
            library_to_save = library or self.library
            with open('music_library.json', 'w', encoding='utf-8') as f:
                json.dump(library_to_save, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando biblioteca: {e}")
    
    def load_playlists(self):
        """Cargar listas de reproducción"""
        try:
            if os.path.exists('playlists.json'):
                with open('playlists.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {}
        except Exception as e:
            print(f"Error cargando playlists: {e}")
            return {}
    
    def save_playlists(self):
        """Guardar listas de reproducción"""
        try:
            with open('playlists.json', 'w', encoding='utf-8') as f:
                json.dump(self.playlists, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando playlists: {e}")
    
    def load_favorites(self):
        """Cargar favoritos"""
        try:
            if os.path.exists('favorites.json'):
                with open('favorites.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return []
        except Exception as e:
            print(f"Error cargando favoritos: {e}")
            return []
    
    def save_favorites(self):
        """Guardar favoritos"""
        try:
            with open('favorites.json', 'w', encoding='utf-8') as f:
                json.dump(self.favorites, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando favoritos: {e}")
    
    def format_time(self, seconds):
        """Formatear tiempo en MM:SS"""
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    def get_song_by_id(self, song_id):
        """Obtener canción por ID"""
        for song in self.library:
            if song['id']
