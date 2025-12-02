import json
import os
import csv
from Track import Track
from Album import AlbumManager

# BST Node for storing tracks
class BSTNode:
    """
    Represent a node in Binary Search Tree for library.
    
    Each node store a track and have left and right child pointers.
    
    Attributes:
        track: The track stored in this node
        left: Left child node with smaller value
        right: Right child node with larger value
    """
    def __init__(self, track):
        self.track = track
        self.left = None
        self.right = None

class Library:
    """
    Manage music library using Binary Search Tree.
    
    This class store all tracks in sorted order and provide search.
    It can import tracks from JSON and CSV files.
    
    Attributes:
        __root: BST root node for store tracks
        __file_path: Path to library JSON file
        __album_manager: Manager for organize tracks into albums
    """
    def __init__(self):
        self.__root = None  # BST root
        self.__file_path = "data/library.json"
        self.__album_manager = AlbumManager()  # Album manager
        self.__load_from_file()
    
    # Compare two tracks based on requirements
    # Returns: -1 if t1 < t2, 0 if equal, 1 if t1 > t2
    def __compare_tracks(self, t1, t2):
        # First compare by title
        if t1.get_title().lower() < t2.get_title().lower():
            return -1
        elif t1.get_title().lower() > t2.get_title().lower():
            return 1
        
        # If titles are same, compare by artist
        artist1 = t1.get_main_artist()
        artist2 = t2.get_main_artist()
        if artist1.lower() < artist2.lower():
            return -1
        elif artist1.lower() > artist2.lower():
            return 1
        
        # If artists are same, compare by album
        if t1.get_album().lower() < t2.get_album().lower():
            return -1
        elif t1.get_album().lower() > t2.get_album().lower():
            return 1
        
        # If albums are same, compare by duration
        if t1.duration_to_seconds() < t2.duration_to_seconds():
            return -1
        elif t1.duration_to_seconds() > t2.duration_to_seconds():
            return 1
        
        return 0  # Completely equal
    
    # Insert track into BST
    def __insert_recursive(self, node, track, inserted_flag):
        if node is None:
            inserted_flag[0] = True  # Mark as inserted
            return BSTNode(track)
        
        comparison = self.__compare_tracks(track, node.track)
        
        if comparison < 0:
            node.left = self.__insert_recursive(node.left, track, inserted_flag)
        elif comparison > 0:
            node.right = self.__insert_recursive(node.right, track, inserted_flag)
        # If comparison == 0, track already exists (don't insert duplicate)
        # inserted_flag remains False
        
        return node
    
    # Add track to library
    def add_track(self, track):
        inserted_flag = [False]  # Use list to pass by reference
        self.__root = self.__insert_recursive(self.__root, track, inserted_flag)
        
        # Only add to album and save if track was actually inserted
        if inserted_flag[0]:
            # Automatically add track to its album
            self.__album_manager.add_track_to_album(track)
            self.__save_to_file()
        
        return inserted_flag[0]  # Return True if inserted, False if duplicate
    
    # Get album manager
    def get_album_manager(self):
        return self.__album_manager
    
    # Get all tracks in sorted order (in-order traversal)
    def __inorder_traversal(self, node, tracks_list):
        if node:
            self.__inorder_traversal(node.left, tracks_list)
            tracks_list.append(node.track)
            self.__inorder_traversal(node.right, tracks_list)
    
    def get_all_tracks(self):
        tracks = []
        self.__inorder_traversal(self.__root, tracks)
        return tracks
    
    # Search for tracks by title (partial match)
    def search_by_title(self, search_term):
        all_tracks = self.get_all_tracks()
        results = []
        for track in all_tracks: # change to log(n) search if needed
            if search_term.lower() in track.get_title().lower():
                results.append(track)
        return results
    
    # Display all tracks with pagination
    def display_library(self, page=1):
        tracks = self.get_all_tracks()
        if not tracks:
            print("Library is empty!")
            return 0
        
        items_per_page = 10
        total_pages = (len(tracks) + items_per_page - 1) // items_per_page
        
        start_idx = (page - 1) * items_per_page
        end_idx = min(start_idx + items_per_page, len(tracks))
        
        print("\n=== MUSIC LIBRARY ===")
        for i in range(start_idx, end_idx):
            print(f"[{i + 1}] {tracks[i].display()}")
        
        if total_pages > 1:
            print(f"\n<Page {page} of {total_pages}>")
        print()
        
        return total_pages
    
    # Save library to JSON file
    def __save_to_file(self):
        tracks = self.get_all_tracks()
        data = [track.to_dict() for track in tracks]
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(self.__file_path), exist_ok=True)
        
        with open(self.__file_path, 'w') as f:
            json.dump(data, f, indent=4)
    
    # Load library from JSON file
    def __load_from_file(self):
        if not os.path.exists(self.__file_path):
            return
        
        try:
            with open(self.__file_path, 'r') as f:
                data = json.load(f)
                for track_data in data:
                    track = Track.from_dict(track_data)
                    inserted_flag = [False]
                    self.__root = self.__insert_recursive(self.__root, track, inserted_flag)
            
            # Load albums after tracks are loaded
            all_tracks = self.get_all_tracks()
            self.__album_manager.load_from_file(all_tracks)
        except:
            print("Error loading library file")
    
    # Get track by index (for selection)
    def get_track_by_index(self, index):
        tracks = self.get_all_tracks()
        if 0 <= index < len(tracks):
            return tracks[index]
        return None
    
    # Import tracks from JSON file
    def import_from_json(self, file_path):
        if not os.path.exists(file_path):
            return {"success": False, "error": "File not found!"}
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            imported = 0
            skipped = 0
            duplicates = 0
            errors = []
            
            for track_data in data:
                try:
                    # Validate required fields
                    if not all(key in track_data for key in ['title', 'artist', 'album', 'duration']):
                        errors.append(f"Missing required fields in track")
                        skipped += 1
                        continue
                    
                    # Handle multiple artists (comma separated in string)
                    artist = track_data['artist']
                    
                    # Create track
                    track = Track(
                        track_data['title'],
                        artist,
                        track_data['album'],
                        track_data['duration']
                    )
                    
                    # Add to library (returns False if duplicate)
                    was_added = self.add_track(track)
                    if was_added:
                        imported += 1
                    else:
                        duplicates += 1
                    
                except Exception as e:
                    errors.append(f"Error with track: {str(e)}")
                    skipped += 1
            
            return {
                "success": True,
                "imported": imported,
                "duplicates": duplicates,
                "skipped": skipped,
                "errors": errors
            }
            
        except json.JSONDecodeError:
            return {"success": False, "error": "Invalid JSON format!"}
        except Exception as e:
            return {"success": False, "error": f"Error reading file: {str(e)}"}
    
    # Import tracks from CSV file
    def import_from_csv(self, file_path):
        if not os.path.exists(file_path):
            return {"success": False, "error": "File not found!"}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                csv_reader = csv.DictReader(f)
                
                imported = 0
                skipped = 0
                duplicates = 0
                errors = []
                
                for row in csv_reader:
                    try:
                        # Validate required fields
                        if not all(key in row for key in ['title', 'artist', 'album', 'duration']):
                            errors.append(f"Missing required fields in row")
                            skipped += 1
                            continue
                        
                        # Handle multiple artists (comma separated)
                        artist = row['artist']
                        if ',' in artist:
                            # Split by comma and strip whitespace
                            artist = [a.strip() for a in artist.split(',')]
                        
                        # Create track
                        track = Track(
                            row['title'].strip(),
                            artist,
                            row['album'].strip(),
                            row['duration'].strip()
                        )
                        
                        # Add to library (returns False if duplicate)
                        was_added = self.add_track(track)
                        if was_added:
                            imported += 1
                        else:
                            duplicates += 1
                        
                    except Exception as e:
                        errors.append(f"Error with row: {str(e)}")
                        skipped += 1
                
                return {
                    "success": True,
                    "imported": imported,
                    "duplicates": duplicates,
                    "skipped": skipped,
                    "errors": errors
                }
                
        except Exception as e:
            return {"success": False, "error": f"Error reading file: {str(e)}"}
    
    # Import tracks (auto-detect format)
    def import_tracks(self, file_path):
        if file_path.lower().endswith('.json'):
            return self.import_from_json(file_path)
        elif file_path.lower().endswith('.csv'):
            return self.import_from_csv(file_path)
        else:
            return {"success": False, "error": "Unsupported file format! Use .json or .csv"}