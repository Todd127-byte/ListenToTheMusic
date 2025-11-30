import json
import os


class Album:
    def __init__(self, album_name):
        self._album_name = album_name
        self._track_list = []

    @property
    def name(self):
        return self._album_name

    @property
    def tracks(self):
        return self._track_list

    @property
    def track_count(self):
        return len(self._track_list)

    def append_track(self, track_obj):
        for existing in self._track_list:
            if existing.matches(track_obj):
                return False
        self._track_list.append(track_obj)
        return True

    def calculate_total_time(self):
        total_secs = sum(t.get_duration_seconds() for t in self._track_list)
        hrs = total_secs // 3600
        mins = (total_secs % 3600) // 60
        secs = total_secs % 60
        if hrs > 0:
            return f"{hrs} hr {mins} min {secs} sec"
        return f"{mins} min {secs} sec"

    def show_info(self):
        print(f"\n=== Album: {self._album_name} ===")
        print(f"Total Tracks: {self.track_count}")
        print(f"Total Duration: {self.calculate_total_time()}")
        print("Tracks:")
        for idx, track in enumerate(self._track_list, 1):
            print(f"    [{idx}] {track.format_display()}")
        print()

    def export_data(self):
        return {"name": self._album_name, "tracks": [t.serialize() for t in self._track_list]}

    @classmethod
    def import_data(cls, album_dict, available_tracks):
        album_obj = cls(album_dict.get("name"))
        for track_data in album_dict.get("tracks", []):
            for track in available_tracks:
                if (track.title == track_data.get("title") and str(track.artist) == str(track_data.get("artist")) and track.album == track_data.get("album")):
                    album_obj.append_track(track)
                    break
        return album_obj


class AlbumCollection:
    def __init__(self):
        self._album_registry = {}
        self._storage_path = "data/albums.json"

    def fetch_or_build_album(self, album_name):
        if album_name not in self._album_registry:
            new_album = Album(album_name)
            self._album_registry[album_name] = new_album
            return new_album
        return self._album_registry[album_name]

    def register_track(self, track_obj):
        album_obj = self.fetch_or_build_album(track_obj.album)
        album_obj.append_track(track_obj)
        self._write_to_disk()

    def fetch_album(self, album_name):
        return self._album_registry.get(album_name)

    def list_album_names(self):
        return list(self._album_registry.keys())

    def retrieve_all_albums(self):
        return list(self._album_registry.values())

    def show_albums(self, page_num=1):
        album_names = self.list_album_names()
        if not album_names:
            print("No albums found!")
            return 0
        items_per_page = 10
        page_count = (len(album_names) + items_per_page - 1) // items_per_page
        start_pos = (page_num - 1) * items_per_page
        end_pos = min(start_pos + items_per_page, len(album_names))
        print("\n=== ALBUMS ===")
        for idx in range(start_pos, end_pos):
            album_obj = self._album_registry[album_names[idx]]
            print(f"[{idx + 1}] {album_names[idx]} ({album_obj.track_count} tracks)")
        if page_count > 1:
            print(f"\n<Page {page_num} of {page_count}>")
        print()
        return page_count

    def fetch_album_at_index(self, position):
        names = self.list_album_names()
        if 0 <= position < len(names):
            return self._album_registry[names[position]]
        return None

    def _write_to_disk(self):
        export_list = [album.export_data() for album in self._album_registry.values()]
        os.makedirs(os.path.dirname(self._storage_path), exist_ok=True)
        with open(self._storage_path, 'w') as file:
            json.dump(export_list, file, indent=4)

    def initialize_from_tracks(self, track_collection):
        if not os.path.exists(self._storage_path):
            return
        try:
            with open(self._storage_path, 'r') as file:
                saved_data = json.load(file)
                for album_entry in saved_data:
                    album_obj = Album.import_data(album_entry, track_collection)
                    self._album_registry[album_obj.name] = album_obj
        except Exception:
            print("Error loading albums file")
import json
import os


class Album:
    def __init__(self, album_name):
        self._album_name = album_name
        self._track_list = []

    @property
    def name(self):
        return self._album_name

    @property
    def tracks(self):
        return self._track_list

    @property
    def track_count(self):
        return len(self._track_list)

    def append_track(self, track_obj):
        for existing in self._track_list:
            if existing.matches(track_obj):
                return False
        self._track_list.append(track_obj)
        return True

    def calculate_total_time(self):
        total_secs = sum(t.get_duration_seconds() for t in self._track_list)
        hrs = total_secs // 3600
        mins = (total_secs % 3600) // 60
        secs = total_secs % 60
        if hrs > 0:
            return f"{hrs} hr {mins} min {secs} sec"
        return f"{mins} min {secs} sec"

    def show_info(self):
        print(f"\n=== Album: {self._album_name} ===")
        print(f"Total Tracks: {self.track_count}")
        print(f"Total Duration: {self.calculate_total_time()}")
        print("Tracks:")
        for idx, track in enumerate(self._track_list, 1):
            print(f"    [{idx}] {track.format_display()}")
        print()

    def export_data(self):
        return {"name": self._album_name, "tracks": [t.serialize() for t in self._track_list]}

    @classmethod
    def import_data(cls, album_dict, available_tracks):
        album_obj = cls(album_dict["name"])
        for track_data in album_dict.get("tracks", []):
            for track in available_tracks:
                if (track.title == track_data.get("title") and str(track.artist) == str(track_data.get("artist")) and track.album == track_data.get("album")):
                    album_obj.append_track(track)
                    break
        return album_obj


class AlbumCollection:
    def __init__(self):
        self._album_registry = {}
        self._storage_path = "data/albums.json"

    def fetch_or_build_album(self, album_name):
        if album_name not in self._album_registry:
            new_album = Album(album_name)
            self._album_registry[album_name] = new_album
            return new_album
        return self._album_registry[album_name]

    def register_track(self, track_obj):
        album_obj = self.fetch_or_build_album(track_obj.album)
        album_obj.append_track(track_obj)
        self._write_to_disk()

    def fetch_album(self, album_name):
        return self._album_registry.get(album_name)

    def list_album_names(self):
        return list(self._album_registry.keys())

    def retrieve_all_albums(self):
        return list(self._album_registry.values())

    def show_albums(self, page_num=1):
        album_names = self.list_album_names()
        if not album_names:
            print("No albums found!")
            return 0
        items_per_page = 10
        page_count = (len(album_names) + items_per_page - 1) // items_per_page
        start_pos = (page_num - 1) * items_per_page
        end_pos = min(start_pos + items_per_page, len(album_names))
        print("\n=== ALBUMS ===")
        for idx in range(start_pos, end_pos):
            album_obj = self._album_registry[album_names[idx]]
            print(f"[{idx + 1}] {album_names[idx]} ({album_obj.track_count} tracks)")
        if page_count > 1:
            print(f"\n<Page {page_num} of {page_count}>")
        print()
        return page_count

    def fetch_album_at_index(self, position):
        names = self.list_album_names()
        if 0 <= position < len(names):
            return self._album_registry[names[position]]
        return None

    def _write_to_disk(self):
        export_list = [album.export_data() for album in self._album_registry.values()]
        os.makedirs(os.path.dirname(self._storage_path), exist_ok=True)
        with open(self._storage_path, 'w') as file:
            json.dump(export_list, file, indent=4)

    def initialize_from_tracks(self, track_collection):
        if not os.path.exists(self._storage_path):
            return
        try:
            with open(self._storage_path, 'r') as file:
                saved_data = json.load(file)
                for album_entry in saved_data:
                    album_obj = Album.import_data(album_entry, track_collection)
                    self._album_registry[album_obj.name] = album_obj
        except Exception:
            print("Error loading albums file")
import json
import os


class Album:
    """
    Represents a collection of tracks under one album name.
    Prevents duplicate tracks automatically.
    """
    def __init__(self, album_name):
        self._album_name = album_name
        self._track_list = []

    @property
    def name(self):
        return self._album_name

    @property
    def tracks(self):
        return self._track_list

    @property
    def track_count(self):
        return len(self._track_list)

    def append_track(self, track_obj):
        """Add track if not already present."""
        for existing in self._track_list:
            if existing.matches(track_obj):
                return False

        self._track_list.append(track_obj)
        return True

    def calculate_total_time(self):
        total_secs = sum(t.get_duration_seconds() for t in self._track_list)

        hrs = total_secs // 3600
        mins = (total_secs % 3600) // 60
        secs = total_secs % 60

        if hrs > 0:
            return f"{hrs} hr {mins} min {secs} sec"
        return f"{mins} min {secs} sec"

    def show_info(self):
        print(f"\n=== Album: {self._album_name} ===")
        print(f"Total Tracks: {self.track_count}")
        print(f"Total Duration: {self.calculate_total_time()}")
        print("Tracks:")

        for idx, track in enumerate(self._track_list, 1):
            print(f"    [{idx}] {track.format_display()}")
        print()

    def export_data(self):
        return {
            "name": self._album_name,
            "tracks": [t.serialize() for t in self._track_list]
        }

    @classmethod
    def import_data(cls, album_dict, available_tracks):
        album_obj = cls(album_dict["name"])

        for track_data in album_dict["tracks"]:
            for track in available_tracks:
                if (track.title == track_data["title"] and
                        str(track.artist) == str(track_data["artist"]) and
                        track.album == track_data["album"]):
                    album_obj.append_track(track)
                    break
        return album_obj


class AlbumCollection:
    """Manages all albums in the system."""

    def __init__(self):
        self._album_registry = {}
        self._storage_path = "data/albums.json"

    def fetch_or_build_album(self, album_name):
        if album_name not in self._album_registry:
            new_album = Album(album_name)
            self._album_registry[album_name] = new_album
            return new_album
        return self._album_registry[album_name]

    def register_track(self, track_obj):
        album_obj = self.fetch_or_build_album(track_obj.album)
        album_obj.append_track(track_obj)
        self._write_to_disk()

    def fetch_album(self, album_name):
        return self._album_registry.get(album_name)

    def list_album_names(self):
        return list(self._album_registry.keys())

    def retrieve_all_albums(self):
        return list(self._album_registry.values())

    def show_albums(self, page_num=1):
        album_names = self.list_album_names()
        if not album_names:
            print("No albums found!")
            return 0

        items_per_page = 10
        page_count = (len(album_names) + items_per_page - 1) // items_per_page

        start_pos = (page_num - 1) * items_per_page
        end_pos = min(start_pos + items_per_page, len(album_names))

        print("\n=== ALBUMS ===")
        for idx in range(start_pos, end_pos):
            album_obj = self._album_registry[album_names[idx]]
            print(f"[{idx + 1}] {album_names[idx]} ({album_obj.track_count} tracks)")

        if page_count > 1:
            print(f"\n<Page {page_num} of {page_count}>")
        print()

        return page_count

    def fetch_album_at_index(self, position):
        names = self.list_album_names()
        if 0 <= position < len(names):
            return self._album_registry[names[position]]
        return None

    def _write_to_disk(self):
        export_list = [album.export_data() for album in self._album_registry.values()]

        os.makedirs(os.path.dirname(self._storage_path), exist_ok=True)

        with open(self._storage_path, 'w') as file:
            json.dump(export_list, file, indent=4)

    def initialize_from_tracks(self, track_collection):
        if not os.path.exists(self._storage_path):
            return

        try:
            with open(self._storage_path, 'r') as file:
                saved_data = json.load(file)
                for album_entry in saved_data:
                    album_obj = Album.import_data(album_entry, track_collection)
                    self._album_registry[album_obj.name] = album_obj
        except Exception:
            print("Error loading albums file")
