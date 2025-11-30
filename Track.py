class Track:
    def __init__(self, title, artist, album, duration):
        self._title = title
        self._artist = artist
        self._album = album
        self._duration = duration

    @property
    def title(self):
        return self._title

    @property
    def artist(self):
        return self._artist

    @property
    def album(self):
        return self._album

    @property
    def duration(self):
        return self._duration

    @title.setter
    def title(self, value):
        self._title = value

    @artist.setter
    def artist(self, value):
        self._artist = value

    @album.setter
    def album(self, value):
        self._album = value

    @duration.setter
    def duration(self, value):
        self._duration = value

    def get_duration_seconds(self):
        if not isinstance(self._duration, str):
            return 0
        parts = [p.strip() for p in self._duration.split(":") if p.strip()]
        try:
            if len(parts) == 2:
                return int(parts[0]) * 60 + int(parts[1])
            if len(parts) == 3:
                return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        except Exception:
            return 0
        return 0

    def primary_artist(self):
        return self._artist[0] if isinstance(self._artist, list) else self._artist

    def format_display(self):
        artist_display = ", ".join(self._artist) if isinstance(self._artist, list) else self._artist
        return f"{self._title} - {artist_display} ({self._duration})"

    def serialize(self):
        return {"title": self._title, "artist": self._artist, "album": self._album, "duration": self._duration}

    @classmethod
    def deserialize(cls, data):
        return cls(data.get("title"), data.get("artist"), data.get("album"), data.get("duration"))

    def matches(self, other):
        if not isinstance(other, Track):
            return False
        return (self._title == other._title and str(self._artist) == str(other._artist) and self._album == other._album and self._duration == other._duration)

    def __repr__(self):
        return self.format_display()
class Track:
    def __init__(self, title, artist, album, duration):
        self._title = title
        self._artist = artist
        self._album = album
        self._duration = duration

    @property
    def title(self):
        return self._title

    @property
    def artist(self):
        return self._artist

    @property
    def album(self):
        return self._album

    @property
    def duration(self):
        return self._duration

    @title.setter
    def title(self, value):
        self._title = value

    @artist.setter
    def artist(self, value):
        self._artist = value

    @album.setter
    def album(self, value):
        self._album = value

    @duration.setter
    def duration(self, value):
        self._duration = value

    def get_duration_seconds(self):
        """Parse duration into seconds supporting mm:ss and hh:mm:ss"""
        if not isinstance(self._duration, str):
            return 0
        parts = [p.strip() for p in self._duration.split(":") if p.strip()]
        try:
            if len(parts) == 2:
                return int(parts[0]) * 60 + int(parts[1])
            if len(parts) == 3:
                return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        except Exception:
            return 0
        return 0

    def primary_artist(self):
        return self._artist[0] if isinstance(self._artist, list) else self._artist

    def format_display(self):
        artist_display = ", ".join(self._artist) if isinstance(self._artist, list) else self._artist
        return f"{self._title} - {artist_display} ({self._duration})"

    def serialize(self):
        return {"title": self._title, "artist": self._artist, "album": self._album, "duration": self._duration}

    @classmethod
    def deserialize(cls, data):
        return cls(data.get("title"), data.get("artist"), data.get("album"), data.get("duration"))

    def matches(self, other):
        if not isinstance(other, Track):
            return False
        return (self._title == other._title and str(self._artist) == str(other._artist) and self._album == other._album and self._duration == other._duration)

    def __repr__(self):
        return self.format_display()
class Track:
    def __init__(self, title, artist, album, duration):
        self._title = title
        self._artist = artist
        self._album = album
        self._duration = duration

    @property
    def title(self):
        return self._title

    @property
    def artist(self):
        return self._artist

    @property
    def album(self):
        return self._album

    @property
    def duration(self):
        return self._duration

    @title.setter
    def title(self, value):
        self._title = value

    @artist.setter
    def artist(self, value):
        self._artist = value

    @album.setter
    def album(self, value):
        self._album = value

    @duration.setter
    def duration(self, value):
        self._duration = value

    def get_duration_seconds(self):
        """Parse duration into seconds.

        Accepts strings like "mm:ss" or "hh:mm:ss" and tolerates surrounding whitespace.
        If parsing fails, returns 0 and prints a short warning.
        """
        if not isinstance(self._duration, str):
            print(f"Warning: track '{self._title}' duration is not a string: {self._duration}")
            return 0

        parts = [p.strip() for p in self._duration.split(":") if p.strip() != ""]

        try:
            if len(parts) == 2:
                minutes = int(parts[0])
                seconds = int(parts[1])
                if minutes < 0 or seconds < 0:
                    raise ValueError()
                return minutes * 60 + seconds
            elif len(parts) == 3:
                hours = int(parts[0])
                minutes = int(parts[1])
                seconds = int(parts[2])
                if hours < 0 or minutes < 0 or seconds < 0:
                    raise ValueError()
                return hours * 3600 + minutes * 60 + seconds
            else:
                raise ValueError()
        except Exception:
            print(f"Warning: couldn't parse duration '{self._duration}' for track '{self._title}', treating as 0s")
            return 0

    def primary_artist(self):
        return self._artist[0] if isinstance(self._artist, list) else self._artist

    def format_display(self):
        artist_display = ", ".join(self._artist) if isinstance(self._artist, list) else self._artist
        return f"{self._title} - {artist_display} ({self._duration})"

    def serialize(self):
        return {
            "title": self._title,
            "artist": self._artist,
            "album": self._album,
            "duration": self._duration,
        }

    @classmethod
    def deserialize(cls, data):
        return cls(data["title"], data["artist"], data["album"], data["duration"])

    def matches(self, other):
        if not isinstance(other, Track):
            return False
        return (self._title == other._title and
                str(self._artist) == str(other._artist) and
                self._album == other._album and
                self._duration == other._duration)

    def __repr__(self):
        return self.format_display()
