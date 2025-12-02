from Library import Library
from Playlist import PlaylistManager
from Queue import MusicQueue
from Track import Track

def main_menu():
    print("\n" + "="*40)
    print("    LISTEN TO THE MUSIC")
    print("="*40)
    print("[1] Music Library")
    print("[2] Playlists")
    print("[3] Music Queue")
    print("[4] Exit")
    print("="*40)

def library_menu():
    print("\n--- MUSIC LIBRARY ---")
    print("[1] Add Track")
    print("[2] View Library")
    print("[3] Search Track")
    print("[4] View Albums")
    print("[5] Import Tracks")
    print("[6] Back")

def playlist_menu():
    print("\n--- PLAYLISTS ---")
    print("[1] Create Playlist")
    print("[2] View Playlists")
    print("[3] Add Track to Playlist")
    print("[4] Create Queue from Playlist")
    print("[5] Import Playlists")
    print("[6] Back")

def queue_menu(is_playing, is_repeat, is_shuffled):
    print("\n--- MUSIC QUEUE ---")
    
    # Dynamic play/pause option
    if is_playing:
        print("[1] Pause")
    else:
        print("[1] Play")
    
    print("[2] Next")
    print("[3] Previous")
    
    # Dynamic repeat option
    if is_repeat:
        print("[4] Turn off repeat")
    else:
        print("[4] Turn on repeat")
    
    # Dynamic shuffle option
    if is_shuffled:
        print("[5] Turn off shuffle")
    else:
        print("[5] Turn on shuffle")
    
    print("[6] Dequeue track")
    print("[7] Clear queue")
    print("[8] Exit queue")

# Initialize components
library = Library()
playlist_manager = PlaylistManager(library)
music_queue = MusicQueue()

def handle_library():
    while True:
        library_menu()
        choice = input("Enter choice: ")
        
        if choice == "1":
            # Add track
            print("\n--- Add New Track ---")
            title = input("Title: ")
            artist_input = input("Artist (separate multiple with comma): ")
            
            # Handle multiple artists
            if "," in artist_input:
                artist = [a.strip() for a in artist_input.split(",")]
            else:
                artist = artist_input.strip()
            
            album = input("Album: ")
            duration = input("Duration (mm:ss): ")
            if ":" not in duration or len(duration.split(":")) != 2:
                print("Invalid duration format! Use mm:ss")
                continue
            
            track = Track(title, artist, album, duration)
            library.add_track(track)
            print("Track added successfully!")
        
        elif choice == "2":
            # View library with pagination
            page = 1
            while True:
                total_pages = library.display_library(page)
                if not total_pages:
                    # Empty library - no options to show
                    input("Press Enter to continue...")
                    break
                elif total_pages == 1:
                    print("[a] Add to queue  |  [b] Back")
                    nav = input("Enter choice: ")
                    if nav.lower() == 'a':
                        try:
                            track_num = int(input("Enter track number to add to queue: "))
                            track = library.get_track_by_index(track_num - 1)
                            if track:
                                was_added = music_queue.add_track(track)
                                if was_added:
                                    music_queue.save_state()
                                    print(f"Added '{track.get_title()}' to queue!")
                                input("Press Enter to continue...")
                            else:
                                print("Invalid track number!")
                        except:
                            print("Invalid input!")
                    elif nav.lower() == 'b':
                        break
                    continue
                
                print("[n] Next  |  [p] Previous  |  [a] Add to queue  |  [b] Back")
                nav = input("Enter choice: ")
                if nav.lower() == 'n' and page < total_pages:
                    page += 1
                elif nav.lower() == 'p' and page > 1:
                    page -= 1
                elif nav.lower() == 'a':
                    try:
                        track_num = int(input("Enter track number to add to queue: "))
                        track = library.get_track_by_index(track_num - 1)
                        if track:
                            was_added = music_queue.add_track(track)
                            if was_added:
                                music_queue.save_state()
                                print(f"Added '{track.get_title()}' to queue!")
                            input("Press Enter to continue...")
                        else:
                            print("Invalid track number!")
                    except:
                        print("Invalid input!")
                elif nav.lower() == 'b':
                    break
        
        elif choice == "3":
            # Search track
            search_term = input("Enter track title to search: ")
            results = library.search_by_title(search_term)
            
            if results:
                print("\n--- Search Results ---")
                for i, track in enumerate(results, 1):
                    print(f"[{i}] {track.display()}")
            else:
                print("No tracks found!")
        
        elif choice == "4":
            # View albums
            album_manager = library.get_album_manager()
            page = 1
            
            while True:
                total_pages = album_manager.display_albums(page)
                if not total_pages:
                    # Empty albums - no options to show
                    break
                
                # Show options
                if total_pages > 1:
                    print("[n] Next  |  [p] Previous  |  [v] View  |  [q] Queue  |  [b] Back")
                    nav = input("Enter choice: ")
                else:
                    print("[v] View  |  [q] Queue  |  [b] Back")
                    nav = input("Enter choice: ")
                
                if nav.lower() == 'n' and page < total_pages:
                    page += 1
                elif nav.lower() == 'p' and page > 1:
                    page -= 1
                elif nav.lower() == 'q':
                    # Create queue from album directly
                    try:
                        album_num = int(input("Enter album number: "))
                        album = album_manager.get_album_by_index(album_num - 1)
                        
                        if album:
                            music_queue.clear()
                            music_queue.load_tracks(album.get_tracks())
                            print(f"Queue created from album '{album.get_name()}'!")
                            input("Press Enter to continue...")
                        else:
                            print("Invalid album number!")
                    except:
                        print("Invalid input!")
                elif nav.lower() == 'v':
                    # View album details and options
                    try:
                        album_num = int(input("Enter album number: "))
                        album = album_manager.get_album_by_index(album_num - 1)
                        
                        if album:
                            album.display()
                            
                            # Show album options
                            print("[q] Queue  |  [b] Back")
                            action = input("Enter choice: ")
                            
                            if action.lower() == 'q':
                                # Create queue from album
                                music_queue.clear()
                                music_queue.load_tracks(album.get_tracks())
                                print(f"Queue created from album '{album.get_name()}'!")
                                input("Press Enter to continue...")
                        else:
                            print("Invalid album number!")
                    except:
                        print("Invalid input!")
                elif nav.lower() == 'b':
                    break
        
        elif choice == "5":
            # Import tracks
            print("\n--- Import Tracks ---")
            print("Place your JSON or CSV files in the 'import/tracks' directory")
            file_name = input("Enter filename (e.g., tracks1.json): ")
            
            # Construct file path
            file_path = f"import/tracks/{file_name}"
            
            print(f"\nImporting from {file_path}...")
            result = library.import_tracks(file_path)
            
            if result["success"]:
                print(f"\n✓ Successfully imported {result['imported']} tracks!")
                
                # Show duplicates
                if result.get('duplicates', 0) > 0:
                    print(f"⚠ {result['duplicates']} track(s) skipped (already exists)")
                
                # Show errors
                if result['skipped'] > 0:
                    print(f"⚠ {result['skipped']} track(s) skipped (errors)")
                    if result['errors']:
                        print("Errors:")
                        for error in result['errors'][:5]:  # Show first 5 errors
                            print(f"  - {error}")
                
                # Show album info
                album_manager = library.get_album_manager()
                total_albums = len(album_manager.get_all_albums())
                print(f"Total albums in library: {total_albums}")
            else:
                print(f"\n✗ Import failed: {result['error']}")
            
            input("\nPress Enter to continue...")
        
        elif choice == "6":
            break

def handle_playlists():
    while True:
        playlist_menu()
        choice = input("Enter choice: ")
        
        if choice == "1":
            # Create playlist
            name = input("Enter playlist name: ")
            result = playlist_manager.create_playlist(name)
            if result:
                print(f"Playlist '{name}' created!")
            else:
                print("Playlist name already exists!")
        
        elif choice == "2":
            # View playlists with pagination and options
            page = 1
            sorted_playlists = None  # Track if we're viewing sorted playlists
            
            while True:
                total_pages = playlist_manager.display_playlists(page, sorted_playlists)
                if not total_pages:
                    # Empty playlists - no options to show
                    break
                
                if total_pages > 1:
                    print("[n] Next  |  [p] Previous  |  [v] View  |  [q] Queue  |  [s] Sort  |  [b] Back")
                    nav = input("Enter choice: ")
                else:
                    print("[v] View  |  [q] Queue  |  [s] Sort  |  [b] Back")
                    nav = input("Enter choice: ")
                
                if nav.lower() == 'n' and page < total_pages:
                    page += 1
                elif nav.lower() == 'p' and page > 1:
                    page -= 1
                elif nav.lower() == 's':
                    # Sort playlists
                    print("\n--- Sort Playlists By ---")
                    print("[1] Date Created")
                    print("[2] Name")
                    print("[3] Duration")
                    print("[4] Back to original order")
                    
                    sort_choice = input("Enter choice: ")
                    
                    if sort_choice == "1":
                        sorted_playlists = playlist_manager.sort_playlists("date_created")
                        print("\nPlaylists sorted by date created!")
                        page = 1  # Reset to first page
                    elif sort_choice == "2":
                        sorted_playlists = playlist_manager.sort_playlists("name")
                        print("\nPlaylists sorted by name!")
                        page = 1
                    elif sort_choice == "3":
                        sorted_playlists = playlist_manager.sort_playlists("duration")
                        print("\nPlaylists sorted by duration!")
                        page = 1
                    elif sort_choice == "4":
                        sorted_playlists = None
                        print("\nBack to original order!")
                        page = 1
                elif nav.lower() == 'q':
                    # Create queue from playlist directly
                    try:
                        playlist_num = int(input("Enter playlist number: "))
                        playlist = playlist_manager.get_playlist_by_index(playlist_num - 1, sorted_playlists)
                        
                        if playlist:
                            music_queue.clear()
                            music_queue.load_tracks(playlist.get_tracks())
                            print(f"Queue created from playlist '{playlist.get_name()}'!")
                            input("Press Enter to continue...")
                        else:
                            print("Invalid playlist number!")
                    except:
                        print("Invalid input!")
                elif nav.lower() == 'v':
                    # View playlist details
                    try:
                        playlist_num = int(input("Enter playlist number: "))
                        playlist = playlist_manager.get_playlist_by_index(playlist_num - 1, sorted_playlists)
                        
                        if playlist:
                            # View playlist loop with sorting options
                            while True:
                                # Display the playlist
                                playlist.display()
                                
                                # Show playlist options with sorting
                                print("[s] Sort  |  [q] Queue  |  [b] Back")
                                action = input("Enter choice: ")
                                
                                if action.lower() == 's':
                                    # Sort tracks in playlist
                                    print("\n--- Sort Tracks By ---")
                                    print("[1] Date added")
                                    print("[2] Title")
                                    print("[3] Artist")
                                    print("[4] Duration")
                                    print("[5] Back")
                                    
                                    sort_choice = input("Enter choice: ")
                                    
                                    if sort_choice == "1":
                                        playlist.sort_tracks("date_added")
                                        print("\nTracks sorted by date added!")
                                    elif sort_choice == "2":
                                        playlist.sort_tracks("title")
                                        print("\nTracks sorted by title!")
                                    elif sort_choice == "3":
                                        playlist.sort_tracks("artist")
                                        print("\nTracks sorted by artist!")
                                    elif sort_choice == "4":
                                        playlist.sort_tracks("duration")
                                        print("\nTracks sorted by duration!")
                                    # Loop continues to show updated playlist
                                    
                                elif action.lower() == 'q':
                                    # Create queue from playlist in current sort order
                                    music_queue.clear()
                                    music_queue.load_tracks(playlist.get_tracks())
                                    print(f"Queue created from playlist '{playlist.get_name()}'!")
                                    input("Press Enter to continue...")
                                    break
                                elif action.lower() == 'b':
                                    break
                        else:
                            print("Invalid playlist number!")
                    except:
                        print("Invalid input!")
                elif nav.lower() == 'b':
                    break
        
        elif choice == "3":
            # Add track to playlist - browse playlists first
            page = 1
            playlist_name = None
            
            # Browse playlists with pagination
            while True:
                total_pages = playlist_manager.display_playlists(page)
                if not total_pages:
                    break
                
                # Show options to select playlist
                if total_pages > 1:
                    print("[n] Next  |  [p] Previous  |  [s] Select playlist  |  [b] Back")
                    nav = input("Enter choice: ")
                else:
                    print("[s] Select playlist  |  [b] Back")
                    nav = input("Enter choice: ")
                
                if nav.lower() == 'n' and page < total_pages:
                    page += 1
                elif nav.lower() == 'p' and page > 1:
                    page -= 1
                elif nav.lower() == 's':
                    # Select playlist by number
                    try:
                        playlist_num = int(input("Enter playlist number: "))
                        playlist = playlist_manager.get_playlist_by_index(playlist_num - 1)
                        
                        if not playlist:
                            print("Invalid playlist number!")
                            continue
                        else:
                            playlist_name = playlist.get_name()
                            break
                    except:
                        print("Invalid input!")
                elif nav.lower() == 'b':
                    break
            
            # If no playlist selected, go back
            if not playlist_name:
                continue
            
            # Now browse library with pagination and allow adding tracks
            page = 1
            while True:
                total_pages = library.display_library(page)
                if not total_pages:
                    break
                
                # Show navigation options
                if total_pages > 1:
                    print("[n] Next  |  [p] Previous  |  [x] Add track  |  [b] Back")
                    nav = input("Enter choice: ")
                else:
                    print("[x] Add track  |  [b] Back")
                    nav = input("Enter choice: ")
                
                if nav.lower() == 'n' and page < total_pages:
                    page += 1
                elif nav.lower() == 'p' and page > 1:
                    page -= 1
                elif nav.lower() == 'x':
                    # Add track
                    try:
                        track_num = int(input("Enter track number to add: "))
                        track = library.get_track_by_index(track_num - 1)
                        
                        if track:
                            if playlist_manager.add_track_to_playlist(playlist_name, track):
                                print("Track added to playlist!")
                            else:
                                print("Track already in playlist!")
                        else:
                            print("Invalid track number!")
                    except:
                        print("Invalid input!")
                elif nav.lower() == 'b':
                    break
        
        elif choice == "4":
            # Create queue from playlist - browse playlists first
            page = 1
            
            # Browse playlists with pagination
            while True:
                total_pages = playlist_manager.display_playlists(page)
                if not total_pages:
                    break
                
                # Show options to select playlist
                if total_pages > 1:
                    print("[n] Next  |  [p] Previous  |  [c] Create queue  |  [b] Back")
                    nav = input("Enter choice: ")
                else:
                    print("[c] Create queue  |  [b] Back")
                    nav = input("Enter choice: ")
                
                if nav.lower() == 'n' and page < total_pages:
                    page += 1
                elif nav.lower() == 'p' and page > 1:
                    page -= 1
                elif nav.lower() == 'c':
                    # Select playlist by number
                    try:
                        playlist_num = int(input("Enter playlist number: "))
                        playlist = playlist_manager.get_playlist_by_index(playlist_num - 1)
                        
                        if playlist:
                            music_queue.clear()
                            music_queue.load_tracks(playlist.get_tracks())
                            print("Queue created from playlist!")
                            input("Press Enter to continue...")
                            break
                        else:
                            print("Invalid playlist number!")
                    except:
                        print("Invalid input!")
                elif nav.lower() == 'b':
                    break
        
        elif choice == "5":
            # Import playlists
            print("\n--- Import Playlists ---")
            print("Place your JSON or CSV files in the 'import/playlists' directory")
            file_name = input("Enter filename (e.g., playlist1.json): ")
            
            # Construct file path
            file_path = f"import/playlists/{file_name}"
            
            print(f"\nImporting from {file_path}...")
            result = playlist_manager.import_playlists(file_path)
            
            if result["success"]:
                print(f"\n✓ Successfully imported {result['imported']} playlist(s)!")
                print("✓ All tracks from playlists have been added to your library!")
                
                # Show duplicates
                if result.get('duplicates', 0) > 0:
                    print(f"⚠ {result['duplicates']} playlist(s) skipped (already exists)")
                
                # Show errors
                if result['skipped'] > 0:
                    print(f"⚠ {result['skipped']} playlist(s) skipped (errors)")
                    if result['errors']:
                        print("Errors:")
                        for error in result['errors'][:5]:  # Show first 5 errors
                            print(f"  - {error}")
            else:
                print(f"\n✗ Import failed: {result['error']}")
            
            input("\nPress Enter to continue...")
        
        elif choice == "6":
            break

def handle_queue():
    # Try to load previous queue state
    music_queue.load_state()
    
    current_page = 1
    
    while True:
        music_queue.display(current_page)
        queue_menu(music_queue.is_playing(), music_queue.is_repeat_on(), music_queue.is_shuffled())
        choice = input("Enter choice: ")
        
        if choice == "1":
            # Toggle play/pause
            if music_queue.is_playing():
                music_queue.pause()
                print("Paused.")
            else:
                music_queue.play()
                print("Playing...")
        
        elif choice == "2":
            # Next
            next_track = music_queue.next_track()
            if next_track:
                print(f"Now playing: {next_track.display()}")
            else:
                print("End of queue!")
        
        elif choice == "3":
            # Previous
            prev_track = music_queue.previous_track()
            if prev_track:
                print(f"Now playing: {prev_track.display()}")
        
        elif choice == "4":
            # Toggle repeat
            repeat_state = music_queue.toggle_repeat()
            print(f"Repeat: {'ON' if repeat_state else 'OFF'}")
        
        elif choice == "5":
            # Toggle shuffle
            if music_queue.is_shuffled():
                music_queue.unshuffle()
                print("Shuffle turned OFF")
            else:
                music_queue.shuffle()
                print("Shuffle turned ON")
        
        elif choice == "6":
            # Dequeue track
            if music_queue.get_size() == 0:
                print("Queue is empty!")
            else:
                # Show all tracks with pagination
                page = 1
                while True:
                    total_pages = music_queue.display_all_tracks(page)
                    
                    if total_pages == 0:
                        break
                    
                    # Show navigation options
                    if total_pages > 1:
                        print("[n] Next  |  [p] Previous  |  [r] Remove track  |  [b] Back")
                        nav = input("Enter choice: ")
                    else:
                        print("[r] Remove track  |  [b] Back")
                        nav = input("Enter choice: ")
                    
                    if nav.lower() == 'n' and page < total_pages:
                        page += 1
                    elif nav.lower() == 'p' and page > 1:
                        page -= 1
                    elif nav.lower() == 'r':
                        try:
                            track_num = int(input("Enter track number to remove: "))
                            if music_queue.remove_track(track_num):
                                print("Track removed from queue!")
                                input("Press Enter to continue...")
                                # Refresh display
                                if music_queue.get_size() == 0:
                                    break
                                # Adjust page if needed
                                total_pages = (music_queue.get_size() + 9) // 10
                                if page > total_pages:
                                    page = total_pages
                            else:
                                print("Invalid track number!")
                                input("Press Enter to continue...")
                        except ValueError:
                            print("Invalid input!")
                            input("Press Enter to continue...")
                    elif nav.lower() == 'b':
                        break
        
        elif choice == "7":
            # Clear queue
            confirm = input("Clear queue? (y/n): ")
            if confirm.lower() == 'y':
                music_queue.clear()
                print("Queue cleared!")
        
        elif choice == "8":
            # Exit queue (saves state automatically)
            break

def main():
    print("Welcome to Listen to the Music!")
    
    while True:
        main_menu()
        choice = input("Enter your choice: ")
        
        if choice == "1":
            handle_library()
        elif choice == "2":
            handle_playlists()
        elif choice == "3":
            handle_queue()
        elif choice == "4":
            print("Thanks for using Listen to the Music!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()