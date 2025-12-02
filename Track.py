import json

class Track:
    def __init__(self, title, artist, album, duration):
        """
        Represent a music track with title, artist, album and duration.
        
        This class store track information and provide methods to access them.
        It support multiple artists and can calculate duration in seconds.
        
        Attributes:
            __title: Track title
            __artist: Artist name or list of artist
            __album: Album name where track belongs
            __duration: Track duration in mm:ss format
        """
        # Private attributes with data encapsulation
        
        self.__title = title
        self.__artist = artist  # can be string or list for multiple artists
        self.__album = album
        self.__duration = duration  # format: "mm:ss"
    
    # Getters for encapsulation
    def get_title(self):
        return self.__title
    
    def get_artist(self):
        return self.__artist
    
    def get_album(self):
        return self.__album
    
    def get_duration(self):
        return self.__duration
 
    # Convert duration to seconds for calculations
    def duration_to_seconds(self):
        try:
            parts = self.__duration.split(":")
            if len(parts) != 2:
                return 0  # Invalid format, return 0
            minutes = int(parts[0])
            seconds = int(parts[1])
            return minutes * 60 + seconds
        except (ValueError, IndexError):
            return 0  # Handle invalid duration format
        
    # Get main artist (for sorting when multiple artists)
    def get_main_artist(self):
        if isinstance(self.__artist, list):
            return self.__artist[0]
        return self.__artist
    
    # Display format
    def display(self):
        artist_str = self.__artist
        if isinstance(self.__artist, list):
            artist_str = ", ".join(self.__artist)
        return f"{self.__title} - {artist_str} ({self.__duration})"
    
    # For saving to JSON
    def to_dict(self):
        return {
            "title": self.__title,
            "artist": self.__artist,
            "album": self.__album,
            "duration": self.__duration
        }
    
    # For loading from JSON
    @staticmethod
    def from_dict(data):
        return Track(data["title"], data["artist"], data["album"], data["duration"])
    
    # Equality check for comparing tracks
    def __eq__(self, other):
        if not isinstance(other, Track):
            return False
        return (self.__title == other.__title and 
                str(self.__artist) == str(other.__artist) and
                self.__album == other.__album and
                self.__duration == other.__duration)
    
    # String representation
    def __str__(self):
        return self.display()