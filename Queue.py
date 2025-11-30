import os
import json
import random
from Track import Track


class MusicQueue:
    def __init__(self, storage='data/queue.json'):
        self._queue = []
        self._current = 0
        self._is_playing = False
        self._repeat = False
        self._shuffled = False
        self._original_order = []
        self._storage = storage

    def append_track(self, track):
        # don't add duplicates
        if any(t.matches(track) for t in self._queue):
            return False
        self._queue.append(track)
        return True

    def load_tracks(self, tracks):
        self._queue = list(tracks)
        self._current = 0
        self._is_playing = False
        self._shuffled = False
        self._original_order = list(self._queue)

    def clear(self):
        self._queue = []
        self._current = 0
        self._is_playing = False
        self._repeat = False
        self._shuffled = False
        self._original_order = []
        try:
            if os.path.exists(self._storage):
                os.remove(self._storage)
        except Exception:
            pass

    def save_state(self):
        try:
            os.makedirs(os.path.dirname(self._storage), exist_ok=True)
            with open(self._storage, 'w') as f:
                json.dump({
                    'queue': [t.serialize() for t in self._queue],
                    'current': self._current,
                    'is_playing': self._is_playing,
                    'repeat': self._repeat,
                    'shuffled': self._shuffled,
                    'original_order': [t.serialize() for t in self._original_order]
                }, f, indent=4)
        except Exception:
            pass

    def load_state(self):
        if not os.path.exists(self._storage):
            return
        try:
            with open(self._storage, 'r') as f:
                data = json.load(f)
                self._queue = [Track.deserialize(d) for d in data.get('queue', [])]
                self._current = data.get('current', 0)
                self._is_playing = data.get('is_playing', False)
                self._repeat = data.get('repeat', False)
                self._shuffled = data.get('shuffled', False)
                original = data.get('original_order', [])
                self._original_order = [Track.deserialize(d) for d in original] if original else list(self._queue)
        except Exception:
            pass

    def display(self, page=1):
        if not self._queue:
            print('\n(Queue is empty)')
            return 0

        per_page = 10
        total_pages = (len(self._queue) + per_page - 1) // per_page

        start = (page - 1) * per_page
        end = min(start + per_page, len(self._queue))

        print('\n=== QUEUE ===')
        for i in range(start, end):
            marker = '>>' if i == self._current else '  '
            print(f"{marker} [{i + 1}] {self._queue[i].format_display()}")

        if total_pages > 1:
            print(f"\n<Page {page} of {total_pages}>")
        print()

        return total_pages

    def is_playing(self):
        return self._is_playing

    def play(self):
        self._is_playing = True

    def pause(self):
        self._is_playing = False

    def next_track(self):
        if not self._queue:
            return None

        if self._current + 1 < len(self._queue):
            self._current += 1
        else:
            if self._repeat:
                self._current = 0
            else:
                return None

        return self._queue[self._current]

    def previous_track(self):
        if not self._queue:
            return None

        if self._current - 1 >= 0:
            self._current -= 1
            return self._queue[self._current]
        else:
            if self._repeat:
                self._current = len(self._queue) - 1
                return self._queue[self._current]
        return None

    def toggle_repeat(self):
        self._repeat = not self._repeat
        return self._repeat

    def is_repeat_on(self):
        return self._repeat

    def shuffle(self):
        if not self._queue:
            return
        if not self._shuffled:
            self._original_order = list(self._queue)
            random.shuffle(self._queue)
            self._shuffled = True

    def unshuffle(self):
        if self._shuffled:
            self._queue = list(self._original_order)
            self._shuffled = False

    def is_shuffled(self):
        return self._shuffled
