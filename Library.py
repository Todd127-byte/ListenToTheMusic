import os
import json
from Track import Track
from Album import AlbumCollection


class MusicLibrary:
    def __init__(self):
        self._tracks = []
        self._storage_path = 'data/tracks.json'
        self._album_collection = AlbumCollection()
        self._load_tracks()

    def _write_to_disk(self):
        os.makedirs(os.path.dirname(self._storage_path), exist_ok=True)
        with open(self._storage_path, 'w') as f:
            json.dump([t.serialize() for t in self._tracks], f, indent=4)

    def _load_tracks(self):
        if not os.path.exists(self._storage_path):
            return

        try:
            with open(self._storage_path, 'r') as f:
                data = json.load(f)
                for item in data:
                    t = Track.deserialize(item)
                    self._tracks.append(t)

            self._album_collection.initialize_from_tracks(self._tracks)
        except Exception:
            print('Error loading library')

    def insert_track(self, track):
        if any(t.matches(track) for t in self._tracks):
            return False
        self._tracks.append(track)
        self._album_collection.register_track(track)
        self._write_to_disk()
        return True

    def show_library(self, page_num=1):
        if not self._tracks:
            print('No tracks in library yet!')
            return 0

        per_page = 10
        total_pages = (len(self._tracks) + per_page - 1) // per_page

        start = (page_num - 1) * per_page
        end = min(start + per_page, len(self._tracks))

        print('\n=== LIBRARY ===')
        for i in range(start, end):
            print(f"[{i + 1}] {self._tracks[i].format_display()}")

        if total_pages > 1:
            print(f"\n<Page {page_num} of {total_pages}>")
        print()

        return total_pages

    def fetch_track_at(self, position):
        return self._tracks[position] if 0 <= position < len(self._tracks) else None

    def find_by_title(self, query):
        q = query.lower()
        return [t for t in self._tracks if q in t.title.lower()]

    def retrieve_album_collection(self):
        return self._album_collection

    def import_tracks(self, filepath):
        try:
            if filepath.lower().endswith('.json'):
                with open(filepath, 'r') as f:
                    data = json.load(f)

                results = {"success": True, "imported": 0, "duplicates": 0, "skipped": 0, "errors": []}

                for entry in data:
                    try:
                        title = entry['title']
                        artist = entry['artist']
                        album = entry['album']
                        duration = entry['duration']

                        track = Track(title, artist, album, duration)
                        if self.insert_track(track):
                            results['imported'] += 1
                        else:
                            results['duplicates'] += 1
                    except Exception as e:
                        results['skipped'] += 1
                        results['errors'].append(str(e))

                return results

            elif filepath.lower().endswith('.csv'):
                import csv

                with open(filepath, 'r') as f:
                    reader = csv.DictReader(f)

                    results = {"success": True, "imported": 0, "duplicates": 0, "skipped": 0, "errors": []}
                    for row in reader:
                        try:
                            title = row['title'].strip()
                            artist = row['artist'].strip()
                            album = row['album'].strip()
                            duration = row['duration'].strip()

                            if "," in artist and not artist.startswith('"'):
                                artist = [a.strip() for a in artist.split(',')]

                            track = Track(title, artist, album, duration)
                            if self.insert_track(track):
                                results['imported'] += 1
                            else:
                                results['duplicates'] += 1
                        except Exception as e:
                            results['skipped'] += 1
                            results['errors'].append(str(e))

                    return results

            else:
                return {"success": False, "error": 'Unsupported file format'}

        except Exception as e:
            return {"success": False, "error": str(e)}
import os
import json
from Track import Track
from Album import AlbumCollection


class MusicLibrary:
    def __init__(self):
        self._tracks = []
        self._storage_path = 'data/tracks.json'
        self._album_collection = AlbumCollection()
        self._load_tracks()

    def _write_to_disk(self):
        os.makedirs(os.path.dirname(self._storage_path), exist_ok=True)
        with open(self._storage_path, 'w') as f:
            json.dump([t.serialize() for t in self._tracks], f, indent=4)

    def _load_tracks(self):
        if not os.path.exists(self._storage_path):
            return

        try:
            with open(self._storage_path, 'r') as f:
                data = json.load(f)
                for item in data:
                    t = Track.deserialize(item)
                    self._tracks.append(t)

            # Populate album collection from loaded tracks
            self._album_collection.initialize_from_tracks(self._tracks)
        except Exception:
            print('Error loading library')

    def insert_track(self, track):
        if any(t.matches(track) for t in self._tracks):
            return False

        self._tracks.append(track)
        # register into albums
        self._album_collection.register_track(track)
        self._write_to_disk()
        return True

    def show_library(self, page_num=1):
        if not self._tracks:
            print('No tracks in library yet!')
            return 0

        per_page = 10
        total_pages = (len(self._tracks) + per_page - 1) // per_page

        start = (page_num - 1) * per_page
        end = min(start + per_page, len(self._tracks))

        print('\n=== LIBRARY ===')
        for i in range(start, end):
            print(f"[{i + 1}] {self._tracks[i].format_display()}")

        if total_pages > 1:
            print(f"\n<Page {page_num} of {total_pages}>")
        print()

        return total_pages

    def fetch_track_at(self, position):
        return self._tracks[position] if 0 <= position < len(self._tracks) else None

    def find_by_title(self, query):
        q = query.lower()
        return [t for t in self._tracks if q in t.title.lower()]

    def retrieve_album_collection(self):
        return self._album_collection

    def import_tracks(self, filepath):
        try:
            if filepath.lower().endswith('.json'):
                with open(filepath, 'r') as f:
                    data = json.load(f)

                results = {"success": True, "imported": 0, "duplicates": 0, "skipped": 0, "errors": []}

                for entry in data:
                    try:
                        title = entry['title']
                        artist = entry['artist']
                        album = entry['album']
                        duration = entry['duration']

                        track = Track(title, artist, album, duration)
                        if self.insert_track(track):
                            results['imported'] += 1
                        else:
                            results['duplicates'] += 1
                    except Exception as e:
                        results['skipped'] += 1
                        results['errors'].append(str(e))

                return results

            elif filepath.lower().endswith('.csv'):
                import csv

                with open(filepath, 'r') as f:
                    reader = csv.DictReader(f)

                    results = {"success": True, "imported": 0, "duplicates": 0, "skipped": 0, "errors": []}
                    for row in reader:
                        try:
                            title = row['title'].strip()
                            artist = row['artist'].strip()
                            album = row['album'].strip()
                            duration = row['duration'].strip()

                            if "," in artist and not artist.startswith('"'):
                                artist = [a.strip() for a in artist.split(',')]

                            track = Track(title, artist, album, duration)
                            if self.insert_track(track):
                                results['imported'] += 1
                            else:
                                results['duplicates'] += 1
                        except Exception as e:
                            results['skipped'] += 1
                            results['errors'].append(str(e))

                    return results

            else:
                return {"success": False, "error": 'Unsupported file format'}

        except Exception as e:
            return {"success": False, "error": str(e)}
