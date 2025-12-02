import json
import os
import random
from Track import Track

# Doubly linked list node for queue
class QueueNode:
    """
    Represent a node in doubly linked list for queue.
    
    Each node store a track and have pointers to next and previous node.
    
    Attributes:
        track: The track stored in this node
        next: Pointer to next node in queue
        prev: Pointer to previous node in queue
    """
    def __init__(self, track: Track):
        self.track = track
        self.next: Track = None
        self.prev: Track = None

class MusicQueue:
    def __init__(self):
        self.__head = None
        self.__tail = None
        self.__current = None  # Currently playing track
        self.__size = 0
        self.__is_shuffled = False
        self.__is_repeat = False
        self.__is_playing = False
        self.__original_order = []  # For unshuffling
        self.__file_path = "data/queue_state.json"
    
    # Add track to queue
    def add_track(self, track: Track):
        curr = self.__head
        while curr is not None:
            if curr.track == track:
                print(f"Track '{track.get_title()}' by '{track.get_artist()}' is already in the queue. Skipping addition.")
                return False  # Duplicate found
            curr = curr.next

        new_node = QueueNode(track)
        
        if self.__head is None:
            self.__head = new_node
            self.__tail = new_node
            self.__current = new_node
        else:
            self.__tail.next = new_node
            new_node.prev = self.__tail
            self.__tail = new_node
        
        self.__size += 1
        # Only add to original_order if not shuffled
        # If shuffled, newly added tracks stay at end and won't be in original order
        if not self.__is_shuffled:
            self.__original_order.append(track)
        return True  # Successfully added
    
    # Load tracks from a list (for creating queue from playlist/library)
    def load_tracks(self, tracks):
        for track in tracks:
            self.add_track(track)
        self.save_state()  # Save after loading tracks
    
    # Play (resume)
    def play(self):
        if not self.__is_repeat and self.__current == self.__tail:
            self.__current = self.__head
        self.__is_playing = True
        self.save_state()
    
    # Pause
    def pause(self):
        self.__is_playing = False
        self.save_state()
    
    # Next track - O(1)
    def next_track(self):
        if not self.__current:
            return None
        
        if self.__current.next:
            self.__current = self.__current.next
        elif self.__is_repeat:
            # If repeat is on, go back to first track
            self.__current = self.__head
        else:
            # No repeat, stop at last track
            self.__is_playing = False
            self.save_state()
            return None
        
        self.save_state()
        return self.__current.track
    
    # Previous track - O(1)
    def previous_track(self):
        if not self.__current:
            return None
        
        if self.__current.prev:
            self.__current = self.__current.prev
        elif self.__is_repeat:
            # If repeat is on and at first track, go to last
            self.__current = self.__tail
        
        self.save_state()
        return self.__current.track
    
    # Shuffle queue
    def shuffle(self):
        if self.__is_shuffled or self.__size <= 1:
            return
        
        # Save original order only on first shuffle (before any tracks were added while shuffled)
        if len(self.__original_order) == 0:
            current = self.__head
            while current:
                self.__original_order.append(current.track)
                current = current.next
        
        # Split tracks into: before current, current, and after current
        before_current = []
        after_current = []
        
        current = self.__head
        found_current = False
        
        while current:
            if not found_current and current != self.__current:
                before_current.append(current.track)
            elif current == self.__current:
                found_current = True
            elif found_current:
                after_current.append(current.track)
            current = current.next
        
        # Remember current track
        current_track = self.__current.track if self.__current else None
        
        # Only shuffle tracks after current
        random.shuffle(after_current)
        
        # Rebuild queue: before + current + shuffled_after
        self.__head = None
        self.__tail = None
        self.__size = 0
        
        # Add tracks before current
        for track in before_current:
            new_node = QueueNode(track)
            if self.__head is None:
                self.__head = new_node
                self.__tail = new_node
            else:
                self.__tail.next = new_node
                new_node.prev = self.__tail
                self.__tail = new_node
            self.__size += 1
        
        # Add current track
        if current_track:
            new_node = QueueNode(current_track)
            if self.__head is None:
                self.__head = new_node
                self.__tail = new_node
                self.__current = new_node
            else:
                self.__tail.next = new_node
                new_node.prev = self.__tail
                self.__tail = new_node
                self.__current = new_node
            self.__size += 1
        
        # Add shuffled tracks after current
        for track in after_current:
            new_node = QueueNode(track)
            if self.__head is None:
                self.__head = new_node
                self.__tail = new_node
            else:
                self.__tail.next = new_node
                new_node.prev = self.__tail
                self.__tail = new_node
            self.__size += 1
        
        # If no current track was found, default to head
        if not self.__current:
            self.__current = self.__head
        
        self.__is_shuffled = True
        self.save_state()
    
    # Unshuffle (restore original order)
    def unshuffle(self):
        if not self.__is_shuffled:
            return
        
        # Remember current track
        current_track = self.__current.track if self.__current else None
        
        # Get tracks that were added during shuffle (not in original_order)
        current = self.__head
        new_tracks = []
        while current:
            if current.track not in self.__original_order:
                new_tracks.append(current.track)
            current = current.next
        
        # pwede ma refactor later(buhaton ug function)
        # Rebuild queue with original order, then append newly added tracks
        self.__head = None
        self.__tail = None
        self.__size = 0
        
        # First restore original order
        for track in self.__original_order:
            new_node = QueueNode(track)
            if self.__head is None:
                self.__head = new_node
                self.__tail = new_node
            else:
                self.__tail.next = new_node
                new_node.prev = self.__tail
                self.__tail = new_node
            self.__size += 1
        
        # Then add tracks that were added during shuffle at the end
        for track in new_tracks:
            new_node = QueueNode(track)
            if self.__head is None:
                self.__head = new_node
                self.__tail = new_node
            else:
                self.__tail.next = new_node
                new_node.prev = self.__tail
                self.__tail = new_node
            self.__size += 1
            self.__original_order.append(track)  # Add to original order now
        
        # Find and set current track
        self.__current = None  # Reset first
        if current_track:
            current = self.__head
            while current:
                if current.track == current_track:
                    self.__current = current
                    break
                current = current.next
        
        # If current track wasn't found, default to head
        if not self.__current:
            self.__current = self.__head
        
        self.__is_shuffled = False
        self.save_state()
    
    # Toggle repeat
    def toggle_repeat(self):
        self.__is_repeat = not self.__is_repeat
        self.save_state()
        return self.__is_repeat
    
    # Remove track from queue by index (1-based)
    def remove_track(self, index):
        if index < 1 or index > self.__size:
            return False
        
        # Find the node at the given index
        current = self.__head
        for i in range(1, index):
            current = current.next
        
        # Track to remove
        track_to_remove = current.track
        
        # Handle removal based on position
        if self.__size == 1:
            # Only one track - clear everything
            self.__head = None
            self.__tail = None
            self.__current = None
        elif current == self.__head:
            # Remove head
            self.__head = current.next
            self.__head.prev = None
            # If removing current, move to next
            if current == self.__current:
                self.__current = self.__head
        elif current == self.__tail:
            # Remove tail
            self.__tail = current.prev
            self.__tail.next = None
            # If removing current (at tail), move to previous
            if current == self.__current:
                self.__current = self.__tail
        else:
            # Remove middle node
            current.prev.next = current.next
            current.next.prev = current.prev
            # If removing current, move to next
            if current == self.__current:
                self.__current = current.next
        
        self.__size -= 1
        
        # Remove from original_order if present
        if track_to_remove in self.__original_order:
            self.__original_order.remove(track_to_remove)
        
        self.save_state()
        return True
    
    # Clear queue
    def clear(self):
        self.__head = None
        self.__tail = None
        self.__current = None
        self.__size = 0
        self.__is_shuffled = False
        self.__is_repeat = False
        self.__is_playing = False
        self.__original_order = []
        self.save_state()
    
    # Get current track
    def get_current_track(self):
        return self.__current.track if self.__current else None
    
    # Get total duration
    def get_total_duration(self):
        total_seconds = 0
        current = self.__head
        while current:
            total_seconds += current.track.duration_to_seconds()
            current = current.next
        
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        return f"{hours} hr {minutes} min"
    
    # Get current page number
    def get_current_page(self):
        if not self.__current:
            return 1
        
        count = 0
        current = self.__head
        while current and current != self.__current:
            count += 1
            current = current.next
        
        return (count // 10) + 1
    
    # Display all tracks in queue (for dequeue selection)
    def display_all_tracks(self, page=1):
        if self.__size == 0:
            print("Queue is empty!")
            return 0
        
        print("\n=== ALL TRACKS IN QUEUE ===")
        print(f"Total tracks: {self.__size}")
        print(f"Total Duration: {self.get_total_duration()}")
        
        items_per_page = 10
        total_pages = (self.__size + items_per_page - 1) // items_per_page
        
        # Get all tracks
        all_tracks = []
        current = self.__head
        while current:
            all_tracks.append(current)
            current = current.next
        
        # Calculate pagination
        start_idx = (page - 1) * items_per_page
        end_idx = min(start_idx + items_per_page, len(all_tracks))
        
        # Display tracks
        print("\nTracks:")
        for i in range(start_idx, end_idx):
            node = all_tracks[i]
            status = " ◄ CURRENT" if node == self.__current else ""
            print(f"    [{i + 1}] {node.track.display()}{status}")
        
        print(f"\n<Page {page} of {total_pages}>")
        return total_pages
    
    # Display queue (first 10 tracks)
    def display(self, page=1):
        if self.__size == 0:
            print("Queue is empty!")
            return
        
        print("\n=== MUSIC QUEUE ===")
        print(f"Total Duration: {self.get_total_duration()}")
        print(f"Shuffled: {'Yes' if self.__is_shuffled else 'No'}")
        print(f"Repeat: {'Yes' if self.__is_repeat else 'No'}")
        print("Tracks:")
        
        # Show current playing
        if self.__current:
            status = "Playing" if self.__is_playing else "Paused"
            print(f"\nCurrently {status}:")
            print(f"    ► {self.__current.track.display()}")
            print("\nUp Next:")
        else:
            print("\nQueue:")
        
        # Calculate page
        items_per_page = 10
        total_pages = (self.__size + items_per_page - 1) // items_per_page
        
        # Get tracks to display
        tracks_list = []
        if self.__current:
            # If there's a current track, show only tracks AFTER it
            current = self.__current.next
            while current:
                tracks_list.append(current)
                current = current.next
            
            # If repeat is on and we've shown all after current, show from beginning to current
            if self.__is_repeat and len(tracks_list) < items_per_page:
                current = self.__head
                while current and current != self.__current:
                    tracks_list.append(current)
                    current = current.next
        else:
            # No current track, show all tracks
            current = self.__head
            while current:
                tracks_list.append(current)
                current = current.next
        
        # Display tracks
        if len(tracks_list) == 0:
            print("    (No more tracks in queue)")
        else:
            start_idx = (page - 1) * items_per_page
            end_idx = min(start_idx + items_per_page, len(tracks_list))
            
            for i in range(start_idx, end_idx):
                node = tracks_list[i]
                print(f"    [{i + 1}] {node.track.display()}")
        
        # Adjust total pages calculation
        if len(tracks_list) > 0:
            total_pages = (len(tracks_list) + items_per_page - 1) // items_per_page
        
        print(f"\n<Page {page} of {total_pages}>")
        print()
    
    # Save queue state
    def save_state(self):
        tracks_data = []
        current = self.__head
        current_index = -1
        idx = 0
        
        while current:
            tracks_data.append(current.track.to_dict())
            if current == self.__current:
                current_index = idx
            current = current.next
            idx += 1
        
        original_data = [t.to_dict() for t in self.__original_order]
        
        state = {
            "tracks": tracks_data,
            "current_index": current_index,
            "is_shuffled": self.__is_shuffled,
            "is_repeat": self.__is_repeat,
            "is_playing": self.__is_playing,
            "original_order": original_data
        }
        
        os.makedirs(os.path.dirname(self.__file_path), exist_ok=True)
        
        with open(self.__file_path, 'w') as f:
            json.dump(state, f, indent=4)
    
    # Load queue state
    def load_state(self):
        if not os.path.exists(self.__file_path):
            return False
        
        try:
            with open(self.__file_path, 'r') as f:
                state = json.load(f)
                
                # Clear current queue
                self.__head = None
                self.__tail = None
                self.__size = 0
                
                # Load tracks
                for track_data in state["tracks"]:
                    track = Track.from_dict(track_data)
                    new_node = QueueNode(track)
                    if self.__head is None:
                        self.__head = new_node
                        self.__tail = new_node
                    else:
                        self.__tail.next = new_node
                        new_node.prev = self.__tail
                        self.__tail = new_node
                    self.__size += 1
                
                # Set current track
                current_index = state["current_index"]
                if current_index >= 0:
                    current = self.__head
                    for i in range(current_index):
                        if current:
                            current = current.next
                    self.__current = current
                
                # Restore state
                self.__is_shuffled = state["is_shuffled"]
                self.__is_repeat = state["is_repeat"]
                self.__is_playing = state["is_playing"]
                
                # Load original order
                self.__original_order = []
                for track_data in state["original_order"]:
                    track = Track.from_dict(track_data)
                    self.__original_order.append(track)
                
                return True
        except:
            return False
    
    # Getters for state
    def is_playing(self):
        return self.__is_playing
    
    def is_shuffled(self):
        return self.__is_shuffled
    
    def is_repeat_on(self):
        return self.__is_repeat
    
    def get_size(self):
        return self.__size