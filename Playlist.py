import json
import os
from datetime import datetime
from Track import Track


class LinkedNode:
    def __init__(self, track_data, timestamp=None):
        self.track_data = track_data
        self.next_node = None
        self.timestamp = timestamp if timestamp else datetime.now()


class MusicPlaylist:
    """Linked list based playlist implementation."""
    def __init__(self, playlist_name, creation_time=None):
        self._playlist_name = playlist_name
        self._first_node = None
        self._track_identifier_set = set()
        self._total_tracks = 0
        self._creation_timestamp = creation_time if creation_time else datetime.now()

    @property
    def name(self):
        return self._playlist_name

    @property
    def size(self):
        return self._total_tracks

    @property
    def created_at(self):
        return self._creation_timestamp

    def _generate_track_id(self, track):
        return track.title.lower() + str(track.artist).lower()

    def _contains_track(self, track):
        return self._generate_track_id(track) in self._track_identifier_set

    def append_track(self, track):
        if self._contains_track(track):
            return False

        new_node = LinkedNode(track)
        self._track_identifier_set.add(self._generate_track_id(track))

        if self._first_node is None:
            self._first_node = new_node
        else:
            current = self._first_node
            while current.next_node:
                current = current.next_node
            current.next_node = new_node

        self._total_tracks += 1
        return True

    def get_all_tracks(self):
        result = []
        current = self._first_node
        while current:
            result.append(current.track_data)
            current = current.next_node
        return result

    def compute_duration(self):
        total_time = 0
        current = self._first_node
        while current:
            total_time += current.track_data.get_duration_seconds()
            current = current.next_node

        hours = total_time // 3600
        minutes = (total_time % 3600) // 60
        seconds = total_time % 60

        if hours > 0:
            return f"{hours} hr {minutes} min {seconds} sec"
        return f"{minutes} min {seconds} sec"

    def show(self):
        print(f"\n=== Playlist: {self._playlist_name} ===")
        print(f"Total Duration: {self.compute_duration()}")
        print("Tracks:")

        current = self._first_node
        counter = 1
        while current:
            print(f"    [{counter}] {current.track_data.format_display()}")
            current = current.next_node
            counter += 1
        print()

    def reorder_tracks(self, sort_criterion="date_added"):
        if self._first_node is None:
            return

        track_timestamp_pairs = []
        current = self._first_node
        while current:
            track_timestamp_pairs.append((current.track_data, current.timestamp))
            current = current.next_node

        def create_sort_key(pair):
            track, timestamp = pair

            if sort_criterion == "date_added":
                return (timestamp, track.title.lower(), track.primary_artist().lower(),
                        track.album.lower(), track.get_duration_seconds())
            elif sort_criterion == "title":
                return (track.title.lower(), track.primary_artist().lower(),
                        track.album.lower(), track.get_duration_seconds(), timestamp)
            elif sort_criterion == "artist":
                return (track.primary_artist().lower(), track.title.lower(),
                        track.album.lower(), track.get_duration_seconds(), timestamp)
            elif sort_criterion == "duration":
                return (track.get_duration_seconds(), track.title.lower(),
                        track.primary_artist().lower(), track.album.lower(), timestamp)

        track_timestamp_pairs.sort(key=create_sort_key)

        self._first_node = None
        for track, timestamp in track_timestamp_pairs:
            node = LinkedNode(track, timestamp)
            if self._first_node is None:
                self._first_node = node
            else:
                current = self._first_node
                while current.next_node:
                    current = current.next_node
                current.next_node = node

    def export(self):
        track_records = []
        current = self._first_node
        while current:
            track_records.append({"track": current.track_data.serialize(), "added_at": current.timestamp.isoformat()})
            current = current.next_node

        return {"name": self._playlist_name, "created_at": self._creation_timestamp.isoformat(), "tracks": track_records}

    @classmethod
    def restore(cls, saved_data):
        creation_time = datetime.fromisoformat(saved_data["created_at"])
        playlist = cls(saved_data["name"], creation_time)

        for track_record in saved_data["tracks"]:
            track = Track.deserialize(track_record["track"])
            timestamp = datetime.fromisoformat(track_record["added_at"])

            node = LinkedNode(track, timestamp)
            playlist._track_identifier_set.add(playlist._generate_track_id(track))

            if playlist._first_node is None:
                playlist._first_node = node
            else:
                current = playlist._first_node
                while current.next_node:
                    current = current.next_node
                current.next_node = node

            playlist._total_tracks += 1

        return playlist


class PlaylistCollection:
    def __init__(self, library_ref=None):
        self._playlists_map = {}
        self._file_location = "data/playlists.json"
        self._library_reference = library_ref
        self._load_playlists()

    def build_playlist(self, playlist_name):
        if playlist_name in self._playlists_map:
            return None

        new_playlist = MusicPlaylist(playlist_name)
        self._playlists_map[playlist_name] = new_playlist
        self._save_playlists()
        return new_playlist

    def fetch_playlist(self, playlist_name):
        return self._playlists_map.get(playlist_name)

    def list_names(self):
        return list(self._playlists_map.keys())

    def fetch_all(self):
        return list(self._playlists_map.values())

    def organize_playlists(self, criterion="date_created"):
        playlists = self.fetch_all()

        if criterion == "date_created":
            playlists.sort(key=lambda p: p.created_at)
        elif criterion == "name":
            playlists.sort(key=lambda p: p.name.lower())
        elif criterion == "duration":
            def calc_seconds(playlist):
                return sum(t.get_duration_seconds() for t in playlist.get_all_tracks())
            playlists.sort(key=calc_seconds)

        return playlists

    def display_page(self, page_num=1, ordered_list=None):
        playlist_list = ordered_list if ordered_list is not None else self.fetch_all()

        if not playlist_list:
            print("No playlists created yet!")
            return 0

        per_page = 10
        total_pages = (len(playlist_list) + per_page - 1) // per_page

        start = (page_num - 1) * per_page
        end = min(start + per_page, len(playlist_list))

        print("\n=== PLAYLISTS ===")
        for i in range(start, end):
            print(f"[{i + 1}] {playlist_list[i].name}")

        if total_pages > 1:
            print(f"\n<Page {page_num} of {total_pages}>")
        print()

        return total_pages

    def fetch_at_position(self, index, ordered_list=None):
        playlist_list = ordered_list if ordered_list is not None else self.fetch_all()
        return playlist_list[index] if 0 <= index < len(playlist_list) else None

    def insert_track(self, playlist_name, track):
        playlist = self.fetch_playlist(playlist_name)
        if playlist:
            success = playlist.append_track(track)
            if success:
                self._save_playlists()
            return success
        return False

    def _save_playlists(self):
        export_data = [p.export() for p in self._playlists_map.values()]

        os.makedirs(os.path.dirname(self._file_location), exist_ok=True)

        with open(self._file_location, 'w') as f:
            json.dump(export_data, f, indent=4)

    def _load_playlists(self):
        if not os.path.exists(self._file_location):
            return

        try:
            with open(self._file_location, 'r') as f:
                saved_data = json.load(f)
                for playlist_data in saved_data:
                    playlist = MusicPlaylist.restore(playlist_data)
                    self._playlists_map[playlist.name] = playlist
        except Exception:
            print("Error loading playlists file")

    def load_from_json(self, filepath):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)

            results = {"success": True, "imported": 0, "duplicates": 0, "skipped": 0, "errors": []}

            for entry in data:
                try:
                    playlist_name = entry.get("name")

                    if not playlist_name:
                        results["skipped"] += 1
                        continue

                    if playlist_name in self._playlists_map:
                        results["duplicates"] += 1
                        continue

                    playlist = self.build_playlist(playlist_name)
                    if not playlist:
                        results["skipped"] += 1
                        continue

                    for track_record in entry.get("tracks", []):
                        track = Track.deserialize(track_record)
                        playlist.append_track(track)
                        if self._library_reference:
                            self._library_reference.insert_track(track)

                    results["imported"] += 1

                except Exception as e:
                    results["errors"].append(f"Error: {str(e)}")
                    results["skipped"] += 1

            self._save_playlists()
            return results

        except Exception as e:
            return {"success": False, "error": f"Error reading file: {str(e)}"}

    def load_from_csv(self, filepath):
        try:
            import csv

            with open(filepath, 'r') as f:
                reader = csv.DictReader(f)

                results = {"success": True, "imported": 0, "duplicates": 0, "skipped": 0, "errors": []}
                temp_playlists = {}

                for row in reader:
                    try:
                        name = row["name"].strip()
                        title = row["title"].strip()
                        artist = row["artist"].strip()
                        album = row["album"].strip()
                        duration = row["duration"].strip()

                        if "," in artist and not artist.startswith('"'):
                            artist = [a.strip() for a in artist.split(',')]

                        track = Track(title, artist, album, duration)

                        if name not in temp_playlists:
                            if name in self._playlists_map:
                                temp_playlists[name] = None
                                results["duplicates"] += 1
                                continue
                            else:
                                playlist = self.build_playlist(name)
                                if playlist:
                                    temp_playlists[name] = playlist
                                    results["imported"] += 1
                                else:
                                    temp_playlists[name] = None
                                    results["skipped"] += 1
                                    continue

                        if temp_playlists[name] is not None:
                            temp_playlists[name].append_track(track)
                            if self._library_reference:
                                self._library_reference.insert_track(track)

                    except Exception as e:
                        results["errors"].append(f"Error: {str(e)}")
                        results["skipped"] += 1

                self._save_playlists()
                return results

        except Exception as e:
            return {"success": False, "error": f"Error reading file: {str(e)}"}

    def import_playlists(self, filepath):
        if filepath.lower().endswith('.json'):
            return self.load_from_json(filepath)
        elif filepath.lower().endswith('.csv'):
            return self.load_from_csv(filepath)
