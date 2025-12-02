import json
import os
from datetime import datetime
from Track import Track

# Simple linked list node for playlist tracks
class PlaylistNode:
    """
    Represent a node in singly linked list for playlist.
    
    Each node store a track with timestamp of when it was added.
    
    Attributes:
        track: The track stored in this node
        next: Pointer to next node in playlist
        added_at: Timestamp when track was added to playlist
    """
    def __init__(self, track, added_at=None):
        self.track = track
        self.next = None
        self.added_at = added_at if added_at else datetime.now()

class Playlist:
    """
    Represent a playlist with tracks in linked list.
    
    Playlists store tracks in order they was added.
    It prevent duplicates and can be sorted by different criteria.
    
    Attributes:
        __name: Playlist name
        __head: First node in linked list
        __track_set: Set for prevent duplicate tracks
        __size: Number of track in playlist
        __created_at: When playlist was created
    """
    def __init__(self, name, created_at=None):
        self.__name = name
        self.__head: PlaylistNode = None  # Linked list of tracks
        self.__track_set = set()  # Hash set for duplicate checking (stores titles)
        self.__size = 0
        self.__created_at = created_at if created_at else datetime.now()
    
    # Getters
    def get_name(self):
        return self.__name
    
    def get_size(self):
        return self.__size
    
    def get_created_at(self):
        return self.__created_at
    
    # Check if track already exists in playlist
    def __has_track(self, track):
        # Simple duplicate check using title + artist
        track_id = track.get_title().lower() + str(track.get_artist()).lower()
        return track_id in self.__track_set
    
    # Add track to playlist
    def add_track(self, track):
        if self.__has_track(track):
            return False  # Track already exists
        
        new_node = PlaylistNode(track)
        track_id = track.get_title().lower() + str(track.get_artist()).lower()
        self.__track_set.add(track_id)
        
        # Add to end of linked list
        if self.__head is None:
            self.__head = new_node
        else:
            current = self.__head
            while current.next:
                current = current.next
            current.next = new_node
        
        self.__size += 1
        return True
    
    # Get all tracks as a list
    def get_tracks(self):
        tracks = []
        current = self.__head
        while current:
            tracks.append(current.track)
            current = current.next
        return tracks
    
    # Calculate total duration
    def get_total_duration(self):
        total_seconds = 0
        current = self.__head
        while current:
            total_seconds += current.track.duration_to_seconds()
            current = current.next
        
        # Convert back to readable format
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        if hours > 0:
            return f"{hours} hr {minutes} min {seconds} sec"
        else:
            return f"{minutes} min {seconds} sec"
    
    # Display playlist
    def display(self):
        print(f"\n=== Playlist: {self.__name} ===")
        print(f"Total Duration: {self.get_total_duration()}")
        print("Tracks:")
        
        current = self.__head
        index = 1
        while current:
            print(f"    [{index}] {current.track.display()}")
            current = current.next
            index += 1
        print()
    
    # Sort tracks in playlist (temporary - only in memory)
    def sort_tracks(self, criteria="date_added"):
        """
        Sort tracks by given criteria.
        criteria: "date_added", "title", "artist", "duration"
        Uses 5-level tie-breaker: title -> artist -> album -> duration -> date
        """
        if self.__head is None:
            return
        
        # Convert linked list to array of (track, added_at) tuples
        tracks_with_dates = []
        current = self.__head
        while current:
            tracks_with_dates.append((current.track, current.added_at))
            current = current.next
        
        # Define sorting key with tie-breaker hierarchy
        def sort_key(item):
            track, added_at = item
            
            if criteria == "date_added":
                return (
                    added_at,
                    track.get_title().lower(),
                    track.get_main_artist().lower(),
                    track.get_album().lower(),
                    track.duration_to_seconds()
                )
            elif criteria == "title":
                return (
                    track.get_title().lower(),
                    track.get_main_artist().lower(),
                    track.get_album().lower(),
                    track.duration_to_seconds(),
                    added_at
                )
            elif criteria == "artist":
                return (
                    track.get_main_artist().lower(),
                    track.get_title().lower(),
                    track.get_album().lower(),
                    track.duration_to_seconds(),
                    added_at
                )
            elif criteria == "duration":
                return (
                    track.duration_to_seconds(),
                    track.get_title().lower(),
                    track.get_main_artist().lower(),
                    track.get_album().lower(),
                    added_at
                )
        
        # Sort the array
        tracks_with_dates.sort(key=sort_key)
        
        # Rebuild linked list with sorted order
        self.__head = None
        for track, added_at in tracks_with_dates:
            new_node = PlaylistNode(track, added_at)
            if self.__head is None:
                self.__head = new_node
            else:
                current = self.__head
                while current.next:
                    current = current.next
                current.next = new_node
    
    # Convert to dictionary for saving
    def to_dict(self):
        tracks_data = []
        current = self.__head
        while current:
            tracks_data.append({
                "track": current.track.to_dict(),
                "added_at": current.added_at.isoformat()
            })
            current = current.next
        
        return {
            "name": self.__name,
            "created_at": self.__created_at.isoformat(),
            "tracks": tracks_data
        }
    
    # Create playlist from dictionary
    @staticmethod
    def from_dict(data):
        created_at = datetime.fromisoformat(data["created_at"])
        playlist = Playlist(data["name"], created_at)
        
        for track_item in data["tracks"]:
            track = Track.from_dict(track_item["track"])
            added_at = datetime.fromisoformat(track_item["added_at"])
            
            # Manually add to maintain timestamp
            new_node = PlaylistNode(track, added_at)
            track_id = track.get_title().lower() + str(track.get_artist()).lower()
            playlist._Playlist__track_set.add(track_id)
            
            if playlist._Playlist__head is None:
                playlist._Playlist__head = new_node
            else:
                current = playlist._Playlist__head
                while current.next:
                    current = current.next
                current.next = new_node
            
            playlist._Playlist__size += 1
        
        return playlist
    
# Playlist Manager to handle multiple playlists                                           
class PlaylistManager:
    """
    Manage all playlists in the system.
    
    This class create, save and load playlists from files.
    It support importing from JSON and CSV format.
    
    Attributes:
        __playlists: Dictionary mapping name to playlist
        __file_path: Path to playlists JSON file
        __library: Reference to library for add imported tracks
    """
    def __init__(self, library=None):
        self.__playlists = {}  # Hash map: name -> Playlist
        self.__file_path = "data/playlists.json"
        self.__library = library  # Reference to Library for auto-adding tracks
        self.__load_from_file()
    
    # Create new playlist
    def create_playlist(self, name):
        if name in self.__playlists:
            return None  # Playlist name already exists
        
        playlist = Playlist(name)
        self.__playlists[name] = playlist
        self.__save_to_file()
        return playlist
    
    # Get playlist by name
    def get_playlist(self, name):
        return self.__playlists.get(name)
    
    # Get all playlist names
    def get_playlist_names(self):
        return list(self.__playlists.keys())
    
    # Get all playlists (for sorting)
    def get_all_playlists(self):
        return list(self.__playlists.values())
    
    # Sort playlists and return sorted list
    def sort_playlists(self, criteria="date_created"):
        """
        Sort playlists by given criteria and return sorted list.
        criteria: "date_created", "name", "duration"
        """
        playlists = self.get_all_playlists()
        
        if criteria == "date_created":
            playlists.sort(key=lambda p: p.get_created_at())
        elif criteria == "name":
            playlists.sort(key=lambda p: p.get_name().lower())
        elif criteria == "duration":
            # Sort by total seconds (calculate duration for each)
            def get_duration_seconds(playlist):
                total = 0
                for track in playlist.get_tracks():
                    total += track.duration_to_seconds()
                return total
            playlists.sort(key=get_duration_seconds)
        
        return playlists
    
    # Display all playlists with pagination
    def display_playlists(self, page=1, sorted_playlists=None):
        """
        Display playlists with pagination.
        If sorted_playlists is provided, use that order instead of default.
        """
        if sorted_playlists is not None:
            playlists = sorted_playlists
        else:
            playlists = self.get_all_playlists()
        
        if not playlists:
            print("No playlists created yet!")
            return
        
        items_per_page = 10
        total_pages = (len(playlists) + items_per_page - 1) // items_per_page
        
        start_idx = (page - 1) * items_per_page
        end_idx = min(start_idx + items_per_page, len(playlists))
        
        print("\n=== PLAYLISTS ===")
        for i in range(start_idx, end_idx):
            print(f"[{i + 1}] {playlists[i].get_name()}")
        
        if total_pages > 1:
            print(f"\n<Page {page} of {total_pages}>")
        print()
        
        return total_pages
    
    # Get playlist by index (for selection)
    def get_playlist_by_index(self, index, sorted_playlists=None):
        """
        Get playlist by index.
        If sorted_playlists is provided, use that order instead of default.
        """
        if sorted_playlists is not None:
            playlists = sorted_playlists
        else:
            playlists = self.get_all_playlists()
        
        if 0 <= index < len(playlists):
            return playlists[index]
        return None
    
    # Add track to specific playlist
    def add_track_to_playlist(self, playlist_name, track):
        playlist = self.get_playlist(playlist_name)
        if playlist:
            result = playlist.add_track(track)
            if result:
                self.__save_to_file()
            return result
        return False
    
    # Save all playlists to file
    def __save_to_file(self):
        data = []
        for playlist in self.__playlists.values():
            data.append(playlist.to_dict())
        
        os.makedirs(os.path.dirname(self.__file_path), exist_ok=True)
        
        with open(self.__file_path, 'w') as f:
            json.dump(data, f, indent=4)
    
    # Load playlists from file
    def __load_from_file(self):
        if not os.path.exists(self.__file_path):
            return
        
        try:
            with open(self.__file_path, 'r') as f:
                data = json.load(f)
                for playlist_data in data:
                    playlist = Playlist.from_dict(playlist_data)
                    self.__playlists[playlist.get_name()] = playlist
        except:
            print("Error loading playlists file")
    
    # Import playlists from JSON file
    def import_from_json(self, file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                
                imported = 0
                duplicates = 0
                skipped = 0
                errors = []
                
                for playlist_data in data:
                    try:
                        name = playlist_data["name"]
                        
                        # Check if playlist already exists
                        if name in self.__playlists:
                            duplicates += 1
                            continue
                        
                        # Create new playlist
                        playlist = self.create_playlist(name)
                        if not playlist:
                            skipped += 1
                            continue
                        
                        # Add tracks to playlist
                        for track_data in playlist_data["tracks"]:
                            track = Track.from_dict(track_data)
                            playlist.add_track(track)
                            # Automatically add track to library if library reference exists
                            if self.__library:
                                self.__library.add_track(track)
                        
                        imported += 1
                        
                    except Exception as e:
                        errors.append(f"Error with playlist: {str(e)}")
                        skipped += 1
                
                self.__save_to_file()
                
                return {
                    "success": True,
                    "imported": imported,
                    "duplicates": duplicates,
                    "skipped": skipped,
                    "errors": errors
                }
                
        except Exception as e:
            return {"success": False, "error": f"Error reading file: {str(e)}"}
    
    # Import playlists from CSV file
    def import_from_csv(self, file_path):
        try:
            import csv
            
            with open(file_path, 'r') as f:
                reader = csv.DictReader(f)
                
                imported = 0
                duplicates = 0
                skipped = 0
                errors = []
                playlists_cache = {}  # Track playlists we're building
                
                for row in reader:
                    try:
                        name = row["name"].strip()
                        title = row["title"].strip()
                        artist = row["artist"].strip()
                        album = row["album"].strip()
                        duration = row["duration"].strip()
                        
                        # Parse multi-artist
                        if "," in artist and not artist.startswith('"'):
                            artist = [a.strip() for a in artist.split(",")]
                        
                        # Create track
                        track = Track(title, artist, album, duration)
                        
                        # Get or create playlist
                        if name not in playlists_cache:
                            if name in self.__playlists:
                                # Playlist already exists, mark as duplicate
                                playlists_cache[name] = None  # Mark as duplicate
                                duplicates += 1
                                continue
                            else:
                                playlist = self.create_playlist(name)
                                if playlist:
                                    playlists_cache[name] = playlist
                                    imported += 1
                                else:
                                    playlists_cache[name] = None
                                    skipped += 1
                                    continue
                        
                        # Add track to playlist (if not duplicate)
                        if playlists_cache[name] is not None:
                            playlists_cache[name].add_track(track)
                            # Automatically add track to library if library reference exists
                            if self.__library:
                                self.__library.add_track(track)
                        
                    except Exception as e:
                        errors.append(f"Error with row: {str(e)}")
                        skipped += 1
                
                self.__save_to_file()
                
                return {
                    "success": True,
                    "imported": imported,
                    "duplicates": duplicates,
                    "skipped": skipped,
                    "errors": errors
                }
                
        except Exception as e:
            return {"success": False, "error": f"Error reading file: {str(e)}"}
    
    # Import playlists (auto-detect format) 
    def import_playlists(self, file_path):
        if file_path.lower().endswith('.json'):
            return self.import_from_json(file_path)
        elif file_path.lower().endswith('.csv'):
            return self.import_from_csv(file_path)
        else:
            return {"success": False, "error": "Unsupported file format! Use .json or .csv"}