import json
import os

class Album:
    """
    Represent a music album with collection of tracks.
    
    Albums group tracks by name and calculate total duration.
    Duplicate tracks is not allowed in same album.
    
    Attributes:
        __name: Album name
        __tracks: List of track in the album
    """
    def __init__(self, name):
        self.__name = name
        self.__tracks = []  # List of tracks in this album
    
    # Getters
    def get_name(self):
        return self.__name
    
    def get_tracks(self):
        return self.__tracks
    
    def get_track_count(self):
        return len(self.__tracks)
    
    # Add track to album
    def add_track(self, track):
        # Check if track already exists in album
        for t in self.__tracks:
            if t == track:
                return False
        
        self.__tracks.append(track)
        return True
    
    # Calculate total duration of album
    def get_total_duration(self):
        total_seconds = 0
        for track in self.__tracks:
            total_seconds += track.duration_to_seconds()
        
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        if hours > 0:
            return f"{hours} hr {minutes} min {seconds} sec"
        else:
            return f"{minutes} min {seconds} sec"
    
    # Display album info
    def display(self):
        print(f"\n=== Album: {self.__name} ===")
        print(f"Total Tracks: {self.get_track_count()}")
        print(f"Total Duration: {self.get_total_duration()}")
        print("Tracks:")
        
        for i, track in enumerate(self.__tracks, 1):
            print(f"    [{i}] {track.display()}")
        print()
    
    # Convert to dictionary for saving
    def to_dict(self):
        return {
            "name": self.__name,
            "tracks": [track.to_dict() for track in self.__tracks]
        }
    
    # Create album from dictionary
    @staticmethod
    def from_dict(data, track_objects):
        album = Album(data["name"])
        # Match tracks by comparing with track objects
        for track_data in data["tracks"]:
            for track in track_objects:
                if (track.get_title() == track_data["title"] and
                    str(track.get_artist()) == str(track_data["artist"]) and
                    track.get_album() == track_data["album"]):
                    album.add_track(track)
                    break
        return album


# Album Manager to handle all albums
class AlbumManager:
    def __init__(self):
        self.__albums = {}  # Hash map: album name -> Album object
        self.__file_path = "data/albums.json"
    
    # Get or create album
    def get_or_create_album(self, album_name):
        if album_name not in self.__albums:
            # Create new album
            album = Album(album_name)
            self.__albums[album_name] = album
            return album
        return self.__albums[album_name]
    
    # Add track to appropriate album
    def add_track_to_album(self, track):
        album_name = track.get_album()
        album = self.get_or_create_album(album_name)
        album.add_track(track)
        self.__save_to_file()
    
    # Get album by name
    def get_album(self, name):
        return self.__albums.get(name)
    
    # Get all album names
    def get_album_names(self):
        return list(self.__albums.keys())
    
    # Get all albums
    def get_all_albums(self):
        return list(self.__albums.values())
    
    # Display all albums with pagination
    def display_albums(self, page=1):
        names = self.get_album_names()
        if not names:
            print("No albums found!")
            return 0
        
        items_per_page = 10
        total_pages = (len(names) + items_per_page - 1) // items_per_page
        
        start_idx = (page - 1) * items_per_page
        end_idx = min(start_idx + items_per_page, len(names))
        
        print("\n=== ALBUMS ===")
        for i in range(start_idx, end_idx):
            album = self.__albums[names[i]]
            print(f"[{i + 1}] {names[i]} ({album.get_track_count()} tracks)")
        
        if total_pages > 1:
            print(f"\n<Page {page} of {total_pages}>")
        print()
        
        return total_pages
    
    # Get album by index
    def get_album_by_index(self, index):
        names = self.get_album_names()
        if 0 <= index < len(names):
            return self.__albums[names[index]]
        return None
    
    # Save albums to file
    def __save_to_file(self):
        data = []
        for album in self.__albums.values():
            data.append(album.to_dict())
        
        os.makedirs(os.path.dirname(self.__file_path), exist_ok=True)
        
        with open(self.__file_path, 'w') as f:
            json.dump(data, f, indent=4)
    
    # Load albums from file
    def load_from_file(self, track_objects):
        if not os.path.exists(self.__file_path):
            return
        
        try:
            with open(self.__file_path, 'r') as f:
                data = json.load(f)
                for album_data in data:
                    album = Album.from_dict(album_data, track_objects)
                    self.__albums[album.get_name()] = album
        except:
            print("Error loading albums file")