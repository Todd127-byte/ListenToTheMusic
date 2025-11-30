from Library import MusicLibrary
from Playlist import PlaylistCollection
from Queue import MusicQueue
from Track import Track

def show_main_menu():
    print("\n" + "="*40)
    print("    LISTEN TO THE MUSIC")
    print("="*40)
    print("[1] Music Library")
    print("[2] Playlists")
    print("[3] Music Queue")
    print("[4] Exit")
    print("="*40)

def show_library_menu():
    print("\n--- MUSIC LIBRARY ---")
    print("[1] Add Track")
    print("[2] View Library")
    print("[3] Search Track")
    print("[4] View Albums")
    print("[5] Import Tracks")
    print("[6] Back")

def show_playlist_menu():
    print("\n--- PLAYLISTS ---")
    print("[1] Create Playlist")
    print("[2] View Playlists")
    print("[3] Add Track to Playlist")
    print("[4] Create Queue from Playlist")
    print("[5] Import Playlists")
    print("[6] Back")

def show_queue_menu(playing, repeating, shuffling):
    print("\n--- MUSIC QUEUE ---")
    print("[1] Pause" if playing else "[1] Play")
    print("[2] Next")
    print("[3] Previous")
    print("[4] Turn off repeat" if repeating else "[4] Turn on repeat")
    print("[5] Turn off shuffle" if shuffling else "[5] Turn on shuffle")
    print("[6] Clear queue")
    print("[7] Exit queue")

# Initialize system components
music_library = MusicLibrary()
playlist_collection = PlaylistCollection(music_library)
queue_system = MusicQueue()

def process_library_actions():
    while True:
        show_library_menu()
        user_choice = input("Enter choice: ")

        if user_choice == "1":
            print("\n--- Add New Track ---")
            track_title = input("Title: ")
            artist_input = input("Artist (separate multiple with comma): ")

            artist_data = [a.strip() for a in artist_input.split(",")] if "," in artist_input else artist_input.strip()

            album_name = input("Album: ")
            time_duration = input("Duration (mm:ss): ")

            if ":" not in time_duration or len(time_duration.split(":")) != 2:
                print("Invalid duration format! Use mm:ss")
                continue

            new_track = Track(track_title, artist_data, album_name, time_duration)
            music_library.insert_track(new_track)
            print("Track added successfully!")

        elif user_choice == "2":
            current_page = 1
            while True:
                page_count = music_library.show_library(current_page)
                if not page_count:
                    input("Press Enter to continue...")
                    break
                elif page_count == 1:
                    print("[a] Add to queue  |  [b] Back")
                    nav_choice = input("Enter choice: ")
                    if nav_choice.lower() == 'a':
                        try:
                            track_idx = int(input("Enter track number to add to queue: "))
                            selected_track = music_library.fetch_track_at(track_idx - 1)
                            if selected_track:
                                added = queue_system.append_track(selected_track)
                                if added:
                                    queue_system.save_state()
                                    print(f"Added '{selected_track.title}' to queue!")
                                input("Press Enter to continue...")
                            else:
                                print("Invalid track number!")
                        except:
                            print("Invalid input!")
                    elif nav_choice.lower() == 'b':
                        break
                    continue

                print("[n] Next  |  [p] Previous  |  [a] Add to queue  |  [b] Back")
                nav_choice = input("Enter choice: ")
                if nav_choice.lower() == 'n' and current_page < page_count:
                    current_page += 1
                elif nav_choice.lower() == 'p' and current_page > 1:
                    current_page -= 1
                elif nav_choice.lower() == 'a':
                    try:
                        track_idx = int(input("Enter track number to add to queue: "))
                        selected_track = music_library.fetch_track_at(track_idx - 1)
                        if selected_track:
                            added = queue_system.append_track(selected_track)
                            if added:
                                queue_system.save_state()
                                print(f"Added '{selected_track.title}' to queue!")
                            input("Press Enter to continue...")
                        else:
                            print("Invalid track number!")
                    except:
                        print("Invalid input!")
                elif nav_choice.lower() == 'b':
                    break

        elif user_choice == "3":
            search_query = input("Enter track title to search: ")
            found_tracks = music_library.find_by_title(search_query)

            if found_tracks:
                print("\n--- Search Results ---")
                for idx, track in enumerate(found_tracks, 1):
                    print(f"[{idx}] {track.format_display()}")
            else:
                print("No tracks found!")

        elif user_choice == "4":
            album_system = music_library.retrieve_album_collection()
            current_page = 1

            while True:
                page_count = album_system.show_albums(current_page)
                if not page_count:
                    break

                if page_count > 1:
                    print("[n] Next  |  [p] Previous  |  [v] View  |  [q] Queue  |  [b] Back")
                    nav_choice = input("Enter choice: ")
                else:
                    print("[v] View  |  [q] Queue  |  [b] Back")
                    nav_choice = input("Enter choice: ")

                if nav_choice.lower() == 'n' and current_page < page_count:
                    current_page += 1
                elif nav_choice.lower() == 'p' and current_page > 1:
                    current_page -= 1
                elif nav_choice.lower() == 'q':
                    try:
                        album_idx = int(input("Enter album number: "))
                        selected_album = album_system.fetch_album_at_index(album_idx - 1)

                        if selected_album:
                            queue_system.clear()
                            queue_system.load_tracks(selected_album.tracks)
                            print(f"Queue created from album '{selected_album.name}'!")
                            input("Press Enter to continue...")
                        else:
                            print("Invalid album number!")
                    except:
                        print("Invalid input!")
                elif nav_choice.lower() == 'v':
                    try:
                        album_idx = int(input("Enter album number: "))
                        selected_album = album_system.fetch_album_at_index(album_idx - 1)

                        if selected_album:
                            selected_album.show_info()

                            print("[q] Queue  |  [b] Back")
                            action = input("Enter choice: ")

                            if action.lower() == 'q':
                                queue_system.clear()
                                queue_system.load_tracks(selected_album.tracks)
                                print(f"Queue created from album '{selected_album.name}'!")
                                input("Press Enter to continue...")
                        else:
                            print("Invalid album number!")
                    except:
                        print("Invalid input!")
                elif nav_choice.lower() == 'b':
                    break

        elif user_choice == "5":
            print("\n--- Import Tracks ---")
            print("Place your JSON or CSV files in the 'import/tracks' directory")
            filename = input("Enter filename (e.g., tracks1.json): ")

            filepath = f"import/tracks/{filename}"

            print(f"\nImporting from {filepath}...")
            import_result = music_library.import_tracks(filepath)

            if import_result.get("success", False):
                print(f"\n✓ Successfully imported {import_result['imported']} tracks!")

                if import_result.get('duplicates', 0) > 0:
                    print(f"⚠ {import_result['duplicates']} track(s) skipped (already exists)")

                if import_result['skipped'] > 0:
                    print(f"⚠ {import_result['skipped']} track(s) skipped (errors)")
                    if import_result['errors']:
                        print("Errors:")
                        for error in import_result['errors'][:5]:
                            print(f"  - {error}")

                album_system = music_library.retrieve_album_collection()
                total_albums = len(album_system.retrieve_all_albums())
                print(f"Total albums in library: {total_albums}")
            else:
                print(f"\n✗ Import failed: {import_result.get('error')}")

            input("\nPress Enter to continue...")

        elif user_choice == "6":
            break

def process_playlist_actions():
    while True:
        show_playlist_menu()
        user_choice = input("Enter choice: ")

        if user_choice == "1":
            playlist_name = input("Enter playlist name: ")
            created = playlist_collection.build_playlist(playlist_name)
            print(f"Playlist '{playlist_name}' created!" if created else "Playlist name already exists!")

        elif user_choice == "2":
            current_page = 1
            sorted_view = None

            while True:
                page_count = playlist_collection.display_page(current_page, sorted_view)
                if not page_count:
                    break

                if page_count > 1:
                    print("[n] Next  |  [p] Previous  |  [v] View  |  [q] Queue  |  [s] Sort  |  [b] Back")
                    nav_choice = input("Enter choice: ")
                else:
                    print("[v] View  |  [q] Queue  |  [s] Sort  |  [b] Back")
                    nav_choice = input("Enter choice: ")

                if nav_choice.lower() == 'n' and current_page < page_count:
                    current_page += 1
                elif nav_choice.lower() == 'p' and current_page > 1:
                    current_page -= 1
                elif nav_choice.lower() == 's':
                    print("\n--- Sort Playlists By ---")
                    print("[1] Date Created")
                    print("[2] Name")
                    print("[3] Duration")
                    print("[4] Back to original order")

                    sort_option = input("Enter choice: ")

                    if sort_option == "1":
                        sorted_view = playlist_collection.organize_playlists("date_created")
                        print("\nPlaylists sorted by date created!")
                        current_page = 1
                    elif sort_option == "2":
                        sorted_view = playlist_collection.organize_playlists("name")
                        print("\nPlaylists sorted by name!")
                        current_page = 1
                    elif sort_option == "3":
                        sorted_view = playlist_collection.organize_playlists("duration")
                        print("\nPlaylists sorted by duration!")
                        current_page = 1
                    elif sort_option == "4":
                        sorted_view = None
                        print("\nBack to original order!")
                        current_page = 1
                elif nav_choice.lower() == 'q':
                    try:
                        playlist_idx = int(input("Enter playlist number: "))
                        selected_playlist = playlist_collection.fetch_at_position(playlist_idx - 1, sorted_view)

                        if selected_playlist:
                            queue_system.clear()
                            queue_system.load_tracks(selected_playlist.get_all_tracks())
                            print(f"Queue created from playlist '{selected_playlist.name}'!")
                            input("Press Enter to continue...")
                        else:
                            print("Invalid playlist number!")
                    except:
                        print("Invalid input!")
                elif nav_choice.lower() == 'v':
                    try:
                        playlist_idx = int(input("Enter playlist number: "))
                        selected_playlist = playlist_collection.fetch_at_position(playlist_idx - 1, sorted_view)

                        if selected_playlist:
                            while True:
                                selected_playlist.show()

                                print("[s] Sort  |  [q] Queue  |  [b] Back")
                                action = input("Enter choice: ")

                                if action.lower() == 's':
                                    print("\n--- Sort Tracks By ---")
                                    print("[1] Date added")
                                    print("[2] Title")
                                    print("[3] Artist")
                                    print("[4] Duration")
                                    print("[5] Back")

                                    sort_option = input("Enter choice: ")

                                    if sort_option == "1":
                                        selected_playlist.reorder_tracks("date_added")
                                        print("\nTracks sorted by date added!")
                                    elif sort_option == "2":
                                        selected_playlist.reorder_tracks("title")
                                        print("\nTracks sorted by title!")
                                    elif sort_option == "3":
                                        selected_playlist.reorder_tracks("artist")
                                        print("\nTracks sorted by artist!")
                                    elif sort_option == "4":
                                        selected_playlist.reorder_tracks("duration")
                                        print("\nTracks sorted by duration!")

                                elif action.lower() == 'q':
                                    queue_system.clear()
                                    queue_system.load_tracks(selected_playlist.get_all_tracks())
                                    print(f"Queue created from playlist '{selected_playlist.name}'!")
                                    input("Press Enter to continue...")
                                    break
                                elif action.lower() == 'b':
                                    break
                        else:
                            print("Invalid playlist number!")
                    except:
                        print("Invalid input!")
                elif nav_choice.lower() == 'b':
                    break

        elif user_choice == "3":
            current_page = 1
            target_playlist = None

            while True:
                page_count = playlist_collection.display_page(current_page)
                if not page_count:
                    break

                if page_count > 1:
                    print("[n] Next  |  [p] Previous  |  [s] Select playlist  |  [b] Back")
                    nav_choice = input("Enter choice: ")
                else:
                    print("[s] Select playlist  |  [b] Back")
                    nav_choice = input("Enter choice: ")

                if nav_choice.lower() == 'n' and current_page < page_count:
                    current_page += 1
                elif nav_choice.lower() == 'p' and current_page > 1:
                    current_page -= 1
                elif nav_choice.lower() == 's':
                    try:
                        playlist_idx = int(input("Enter playlist number: "))
                        selected = playlist_collection.fetch_at_position(playlist_idx - 1)

                        if not selected:
                            print("Invalid playlist number!")
                            continue
                        else:
                            target_playlist = selected.name
                            break
                    except:
                        print("Invalid input!")
                elif nav_choice.lower() == 'b':
                    break

            if not target_playlist:
                continue

            current_page = 1
            while True:
                page_count = music_library.show_library(current_page)
                if not page_count:
                    break

                if page_count > 1:
                    print("[n] Next  |  [p] Previous  |  [x] Add track  |  [b] Back")
                    nav_choice = input("Enter choice: ")
                else:
                    print("[x] Add track  |  [b] Back")
                    nav_choice = input("Enter choice: ")

                if nav_choice.lower() == 'n' and current_page < page_count:
                    current_page += 1
                elif nav_choice.lower() == 'p' and current_page > 1:
                    current_page -= 1
                elif nav_choice.lower() == 'x':
                    try:
                        track_idx = int(input("Enter track number to add: "))
                        selected_track = music_library.fetch_track_at(track_idx - 1)

                        if selected_track:
                            if playlist_collection.insert_track(target_playlist, selected_track):
                                print("Track added to playlist!")
                            else:
                                print("Track already in playlist!")
                        else:
                            print("Invalid track number!")
                    except:
                        print("Invalid input!")
                elif nav_choice.lower() == 'b':
                    break

        elif user_choice == "4":
            current_page = 1

            while True:
                page_count = playlist_collection.display_page(current_page)
                if not page_count:
                    break

                if page_count > 1:
                    print("[n] Next  |  [p] Previous  |  [c] Create queue  |  [b] Back")
                    nav_choice = input("Enter choice: ")
                else:
                    print("[c] Create queue  |  [b] Back")
                    nav_choice = input("Enter choice: ")

                if nav_choice.lower() == 'n' and current_page < page_count:
                    current_page += 1
                elif nav_choice.lower() == 'p' and current_page > 1:
                    current_page -= 1
                elif nav_choice.lower() == 'c':
                    try:
                        playlist_idx = int(input("Enter playlist number: "))
                        selected_playlist = playlist_collection.fetch_at_position(playlist_idx - 1)

                        if selected_playlist:
                            queue_system.clear()
                            queue_system.load_tracks(selected_playlist.get_all_tracks())
                            print("Queue created from playlist!")
                            input("Press Enter to continue...")
                            break
                        else:
                            print("Invalid playlist number!")
                    except:
                        print("Invalid input!")
                elif nav_choice.lower() == 'b':
                    break

        elif user_choice == "5":
            print("\n--- Import Playlists ---")
            print("Place your JSON or CSV files in the 'import/playlists' directory")
            filename = input("Enter filename (e.g., playlist1.json): ")

            filepath = f"import/playlists/{filename}"

            print(f"\nImporting from {filepath}...")
            import_result = playlist_collection.import_playlists(filepath)

            if import_result.get("success", False):
                print(f"\n✓ Successfully imported {import_result['imported']} playlist(s)!")
                print("✓ All tracks from playlists have been added to your library!")

                if import_result.get('duplicates', 0) > 0:
                    print(f"⚠ {import_result['duplicates']} playlist(s) skipped (already exists)")

                if import_result['skipped'] > 0:
                    print(f"⚠ {import_result['skipped']} playlist(s) skipped (errors)")
                    if import_result['errors']:
                        print("Errors:")
                        for error in import_result['errors'][:5]:
                            print(f"  - {error}")
            else:
                print(f"\n✗ Import failed: {import_result.get('error')}")

            input("\nPress Enter to continue...")

        elif user_choice == "6":
            break

def process_queue_actions():
    queue_system.load_state()

    active_page = 1

    while True:
        queue_system.display(active_page)
        show_queue_menu(queue_system.is_playing(), queue_system.is_repeat_on(), queue_system.is_shuffled())
        user_choice = input("Enter choice: ")

        if user_choice == "1":
            if queue_system.is_playing():
                queue_system.pause()
                print("Paused.")
            else:
                queue_system.play()
                print("Playing...")

        elif user_choice == "2":
            next_item = queue_system.next_track()
            print(f"Now playing: {next_item.format_display()}" if next_item else "End of queue!")

        elif user_choice == "3":
            prev_item = queue_system.previous_track()
            if prev_item:
                print(f"Now playing: {prev_item.format_display()}")

        elif user_choice == "4":
            repeat_status = queue_system.toggle_repeat()
            print(f"Repeat: {'ON' if repeat_status else 'OFF'}")

        elif user_choice == "5":
            if queue_system.is_shuffled():
                queue_system.unshuffle()
                print("Shuffle turned OFF")
            else:
                queue_system.shuffle()
                print("Shuffle turned ON")

        elif user_choice == "6":
            confirmation = input("Clear queue? (y/n): ")
            if confirmation.lower() == 'y':
                queue_system.clear()
                print("Queue cleared!")

        elif user_choice == "7":
            break

def main():
    print("Welcome to Listen to the Music!")

    while True:
        show_main_menu()
        user_input = input("Enter your choice: ")

        if user_input == "1":
            process_library_actions()
        elif user_input == "2":
            process_playlist_actions()
        elif user_input == "3":
            process_queue_actions()
        elif user_input == "4":
            print("Thanks for using Listen to the Music!")
            break
        else:
            print("Invalid choice!")

if __name__ == '__main__':
    main()

def show_main_menu():
    print("\n" + "="*40)
    print("    LISTEN TO THE MUSIC")
    print("="*40)
    print("[1] Music Library")
    print("[2] Playlists")
    print("[3] Music Queue")
    print("[4] Exit")
    print("="*40)

def show_library_menu():
    print("\n--- MUSIC LIBRARY ---")
    print("[1] Add Track")
    print("[2] View Library")
    print("[3] Search Track")
    print("[4] View Albums")
    print("[5] Import Tracks")
    print("[6] Back")

def show_playlist_menu():
    print("\n--- PLAYLISTS ---")
    print("[1] Create Playlist")
    print("[2] View Playlists")
    print("[3] Add Track to Playlist")
    print("[4] Create Queue from Playlist")
    print("[5] Import Playlists")
    print("[6] Back")

def show_queue_menu(playing, repeating, shuffling):
    print("\n--- MUSIC QUEUE ---")
    print("[1] Pause" if playing else "[1] Play")
    print("[2] Next")
    print("[3] Previous")
    print("[4] Turn off repeat" if repeating else "[4] Turn on repeat")
    print("[5] Turn off shuffle" if shuffling else "[5] Turn on shuffle")
    print("[6] Clear queue")
    print("[7] Exit queue")

# Initialize system components
music_library = MusicLibrary()
playlist_collection = PlaylistCollection(music_library)
queue_system = MusicQueue()

def process_library_actions():
    while True:
        show_library_menu()
        user_choice = input("Enter choice: ")

        if user_choice == "1":
            print("\n--- Add New Track ---")
            track_title = input("Title: ")
            artist_input = input("Artist (separate multiple with comma): ")

            artist_data = [a.strip() for a in artist_input.split(",")] if "," in artist_input else artist_input.strip()

            album_name = input("Album: ")
            time_duration = input("Duration (mm:ss): ")

            if ":" not in time_duration or len(time_duration.split(":")) != 2:
                print("Invalid duration format! Use mm:ss")
                continue

            new_track = Track(track_title, artist_data, album_name, time_duration)
            music_library.insert_track(new_track)
            print("Track added successfully!")

        elif user_choice == "2":
            current_page = 1
            while True:
                page_count = music_library.show_library(current_page)
                if not page_count:
                    input("Press Enter to continue...")
                    break
                elif page_count == 1:
                    print("[a] Add to queue  |  [b] Back")
                    nav_choice = input("Enter choice: ")
                    if nav_choice.lower() == 'a':
                        try:
                            track_idx = int(input("Enter track number to add to queue: "))
                            selected_track = music_library.fetch_track_at(track_idx - 1)
                            if selected_track:
                                added = queue_system.append_track(selected_track)
                                if added:
                                    queue_system.save_state()
                                    print(f"Added '{selected_track.title}' to queue!")
                                input("Press Enter to continue...")
                            else:
                                print("Invalid track number!")
                        except:
                            print("Invalid input!")
                    elif nav_choice.lower() == 'b':
                        break
                    continue

                print("[n] Next  |  [p] Previous  |  [a] Add to queue  |  [b] Back")
                nav_choice = input("Enter choice: ")
                if nav_choice.lower() == 'n' and current_page < page_count:
                    current_page += 1
                elif nav_choice.lower() == 'p' and current_page > 1:
                    current_page -= 1
                elif nav_choice.lower() == 'a':
                    try:
                        track_idx = int(input("Enter track number to add to queue: "))
                        selected_track = music_library.fetch_track_at(track_idx - 1)
                        if selected_track:
                            added = queue_system.append_track(selected_track)
                            if added:
                                queue_system.save_state()
                                print(f"Added '{selected_track.title}' to queue!")
                            input("Press Enter to continue...")
                        else:
                            print("Invalid track number!")
                    except:
                        print("Invalid input!")
                elif nav_choice.lower() == 'b':
                    break

        elif user_choice == "3":
            search_query = input("Enter track title to search: ")
            found_tracks = music_library.find_by_title(search_query)

            if found_tracks:
                print("\n--- Search Results ---")
                for idx, track in enumerate(found_tracks, 1):
                    print(f"[{idx}] {track.format_display()}")
            else:
                print("No tracks found!")

        elif user_choice == "4":
            album_system = music_library.retrieve_album_collection()
            current_page = 1

            while True:
                page_count = album_system.show_albums(current_page)
                if not page_count:
                    break

                if page_count > 1:
                    print("[n] Next  |  [p] Previous  |  [v] View  |  [q] Queue  |  [b] Back")
                    nav_choice = input("Enter choice: ")
                else:
                    print("[v] View  |  [q] Queue  |  [b] Back")
                    nav_choice = input("Enter choice: ")

                if nav_choice.lower() == 'n' and current_page < page_count:
                    current_page += 1
                elif nav_choice.lower() == 'p' and current_page > 1:
                    current_page -= 1
                elif nav_choice.lower() == 'q':
                    try:
                        album_idx = int(input("Enter album number: "))
                        selected_album = album_system.fetch_album_at_index(album_idx - 1)

                        if selected_album:
                            queue_system.clear()
                            queue_system.load_tracks(selected_album.tracks)
                            print(f"Queue created from album '{selected_album.name}'!")
                            input("Press Enter to continue...")
                        else:
                            print("Invalid album number!")
                    except:
                        print("Invalid input!")
                elif nav_choice.lower() == 'v':
                    try:
                        album_idx = int(input("Enter album number: "))
                        selected_album = album_system.fetch_album_at_index(album_idx - 1)

                        if selected_album:
                            selected_album.show_info()

                            print("[q] Queue  |  [b] Back")
                            action = input("Enter choice: ")

                            if action.lower() == 'q':
                                queue_system.clear()
                                queue_system.load_tracks(selected_album.tracks)
                                print(f"Queue created from album '{selected_album.name}'!")
                                input("Press Enter to continue...")
                        else:
                            print("Invalid album number!")
                    except:
                        print("Invalid input!")
                elif nav_choice.lower() == 'b':
                    break

        elif user_choice == "5":
            print("\n--- Import Tracks ---")
            print("Place your JSON or CSV files in the 'import/tracks' directory")
            filename = input("Enter filename (e.g., tracks1.json): ")

            filepath = f"import/tracks/{filename}"

            print(f"\nImporting from {filepath}...")
            import_result = music_library.import_tracks(filepath)

            if import_result.get("success", False):
                print(f"\n✓ Successfully imported {import_result['imported']} tracks!")

                if import_result.get('duplicates', 0) > 0:
                    print(f"⚠ {import_result['duplicates']} track(s) skipped (already exists)")

                if import_result['skipped'] > 0:
                    print(f"⚠ {import_result['skipped']} track(s) skipped (errors)")
                    if import_result['errors']:
                        print("Errors:")
                        for error in import_result['errors'][:5]:
                            print(f"  - {error}")

                album_system = music_library.retrieve_album_collection()
                total_albums = len(album_system.retrieve_all_albums())
                print(f"Total albums in library: {total_albums}")
            else:
                print(f"\n✗ Import failed: {import_result.get('error')}")

            input("\nPress Enter to continue...")

        elif user_choice == "6":
            break

def process_playlist_actions():
    while True:
        show_playlist_menu()
        user_choice = input("Enter choice: ")

        if user_choice == "1":
            playlist_name = input("Enter playlist name: ")
            created = playlist_collection.build_playlist(playlist_name)
            print(f"Playlist '{playlist_name}' created!" if created else "Playlist name already exists!")

        elif user_choice == "2":
            current_page = 1
            sorted_view = None

            while True:
                page_count = playlist_collection.display_page(current_page, sorted_view)
                if not page_count:
                    break

                if page_count > 1:
                    print("[n] Next  |  [p] Previous  |  [v] View  |  [q] Queue  |  [s] Sort  |  [b] Back")
                    nav_choice = input("Enter choice: ")
                else:
                    print("[v] View  |  [q] Queue  |  [s] Sort  |  [b] Back")
                    nav_choice = input("Enter choice: ")

                if nav_choice.lower() == 'n' and current_page < page_count:
                    current_page += 1
                elif nav_choice.lower() == 'p' and current_page > 1:
                    current_page -= 1
                elif nav_choice.lower() == 's':
                    print("\n--- Sort Playlists By ---")
                    print("[1] Date Created")
                    print("[2] Name")
                    print("[3] Duration")
                    print("[4] Back to original order")

                    sort_option = input("Enter choice: ")

                    if sort_option == "1":
                        sorted_view = playlist_collection.organize_playlists("date_created")
                        print("\nPlaylists sorted by date created!")
                        current_page = 1
                    elif sort_option == "2":
                        sorted_view = playlist_collection.organize_playlists("name")
                        print("\nPlaylists sorted by name!")
                        current_page = 1
                    elif sort_option == "3":
                        sorted_view = playlist_collection.organize_playlists("duration")
                        print("\nPlaylists sorted by duration!")
                        current_page = 1
                    elif sort_option == "4":
                        sorted_view = None
                        print("\nBack to original order!")
                        current_page = 1
                elif nav_choice.lower() == 'q':
                    try:
                        playlist_idx = int(input("Enter playlist number: "))
                        selected_playlist = playlist_collection.fetch_at_position(playlist_idx - 1, sorted_view)

                        if selected_playlist:
                            queue_system.clear()
                            queue_system.load_tracks(selected_playlist.get_all_tracks())
                            print(f"Queue created from playlist '{selected_playlist.name}'!")
                            input("Press Enter to continue...")
                        else:
                            print("Invalid playlist number!")
                    except:
                        print("Invalid input!")
                elif nav_choice.lower() == 'v':
                    try:
                        playlist_idx = int(input("Enter playlist number: "))
                        selected_playlist = playlist_collection.fetch_at_position(playlist_idx - 1, sorted_view)

                        if selected_playlist:
                            while True:
                                selected_playlist.show()

                                print("[s] Sort  |  [q] Queue  |  [b] Back")
                                action = input("Enter choice: ")

                                if action.lower() == 's':
                                    print("\n--- Sort Tracks By ---")
                                    print("[1] Date added")
                                    print("[2] Title")
                                    print("[3] Artist")
                                    print("[4] Duration")
                                    print("[5] Back")

                                    sort_option = input("Enter choice: ")

                                    if sort_option == "1":
                                        selected_playlist.reorder_tracks("date_added")
                                        print("\nTracks sorted by date added!")
                                    elif sort_option == "2":
                                        selected_playlist.reorder_tracks("title")
                                        print("\nTracks sorted by title!")
                                    elif sort_option == "3":
                                        selected_playlist.reorder_tracks("artist")
                                        print("\nTracks sorted by artist!")
                                    elif sort_option == "4":
                                        selected_playlist.reorder_tracks("duration")
                                        print("\nTracks sorted by duration!")

                                elif action.lower() == 'q':
                                    queue_system.clear()
                                    queue_system.load_tracks(selected_playlist.get_all_tracks())
                                    print(f"Queue created from playlist '{selected_playlist.name}'!")
                                    input("Press Enter to continue...")
                                    break
                                elif action.lower() == 'b':
                                    break
                        else:
                            print("Invalid playlist number!")
                    except:
                        print("Invalid input!")
                elif nav_choice.lower() == 'b':
                    break

        elif user_choice == "3":
            current_page = 1
            target_playlist = None

            while True:
                page_count = playlist_collection.display_page(current_page)
                if not page_count:
                    break

                if page_count > 1:
                    print("[n] Next  |  [p] Previous  |  [s] Select playlist  |  [b] Back")
                    nav_choice = input("Enter choice: ")
                else:
                    print("[s] Select playlist  |  [b] Back")
                    nav_choice = input("Enter choice: ")

                if nav_choice.lower() == 'n' and current_page < page_count:
                    current_page += 1
                elif nav_choice.lower() == 'p' and current_page > 1:
                    current_page -= 1
                elif nav_choice.lower() == 's':
                    try:
                        playlist_idx = int(input("Enter playlist number: "))
                        selected = playlist_collection.fetch_at_position(playlist_idx - 1)

                        if not selected:
                            print("Invalid playlist number!")
                            continue
                        else:
                            target_playlist = selected.name
                            break
                    except:
                        print("Invalid input!")
                elif nav_choice.lower() == 'b':
                    break

            if not target_playlist:
                continue

            current_page = 1
            while True:
                page_count = music_library.show_library(current_page)
                if not page_count:
                    break

                if page_count > 1:
                    print("[n] Next  |  [p] Previous  |  [x] Add track  |  [b] Back")
                    nav_choice = input("Enter choice: ")
                else:
                    print("[x] Add track  |  [b] Back")
                    nav_choice = input("Enter choice: ")

                if nav_choice.lower() == 'n' and current_page < page_count:
                    current_page += 1
                elif nav_choice.lower() == 'p' and current_page > 1:
                    current_page -= 1
                elif nav_choice.lower() == 'x':
                    try:
                        track_idx = int(input("Enter track number to add: "))
                        selected_track = music_library.fetch_track_at(track_idx - 1)

                        if selected_track:
                            if playlist_collection.insert_track(target_playlist, selected_track):
                                print("Track added to playlist!")
                            else:
                                print("Track already in playlist!")
                        else:
                            print("Invalid track number!")
                    except:
                        print("Invalid input!")
                elif nav_choice.lower() == 'b':
                    break

        elif user_choice == "4":
            current_page = 1

            while True:
                page_count = playlist_collection.display_page(current_page)
                if not page_count:
                    break

                if page_count > 1:
                    print("[n] Next  |  [p] Previous  |  [c] Create queue  |  [b] Back")
                    nav_choice = input("Enter choice: ")
                else:
                    print("[c] Create queue  |  [b] Back")
                    nav_choice = input("Enter choice: ")

                if nav_choice.lower() == 'n' and current_page < page_count:
                    current_page += 1
                elif nav_choice.lower() == 'p' and current_page > 1:
                    current_page -= 1
                elif nav_choice.lower() == 'c':
                    try:
                        playlist_idx = int(input("Enter playlist number: "))
                        selected_playlist = playlist_collection.fetch_at_position(playlist_idx - 1)

                        if selected_playlist:
                            queue_system.clear()
                            queue_system.load_tracks(selected_playlist.get_all_tracks())
                            print("Queue created from playlist!")
                            input("Press Enter to continue...")
                            break
                        else:
                            print("Invalid playlist number!")
                    except:
                        print("Invalid input!")
                elif nav_choice.lower() == 'b':
                    break

        elif user_choice == "5":
            print("\n--- Import Playlists ---")
            print("Place your JSON or CSV files in the 'import/playlists' directory")
            filename = input("Enter filename (e.g., playlist1.json): ")

            filepath = f"import/playlists/{filename}"

            print(f"\nImporting from {filepath}...")
            import_result = playlist_collection.import_playlists(filepath)

            if import_result.get("success", False):
                print(f"\n✓ Successfully imported {import_result['imported']} playlist(s)!")
                print("✓ All tracks from playlists have been added to your library!")

                if import_result.get('duplicates', 0) > 0:
                    print(f"⚠ {import_result['duplicates']} playlist(s) skipped (already exists)")

                if import_result['skipped'] > 0:
                    print(f"⚠ {import_result['skipped']} playlist(s) skipped (errors)")
                    if import_result['errors']:
                        print("Errors:")
                        for error in import_result['errors'][:5]:
                            print(f"  - {error}")
            else:
                print(f"\n✗ Import failed: {import_result.get('error')}")

            input("\nPress Enter to continue...")

        elif user_choice == "6":
            break

def process_queue_actions():
    queue_system.load_state()

    active_page = 1

    while True:
        queue_system.display(active_page)
        show_queue_menu(queue_system.is_playing(), queue_system.is_repeat_on(), queue_system.is_shuffled())
        user_choice = input("Enter choice: ")

        if user_choice == "1":
            if queue_system.is_playing():
                queue_system.pause()
                print("Paused.")
            else:
                queue_system.play()
                print("Playing...")

        elif user_choice == "2":
            next_item = queue_system.next_track()
            print(f"Now playing: {next_item.format_display()}" if next_item else "End of queue!")

        elif user_choice == "3":
            prev_item = queue_system.previous_track()
            if prev_item:
                print(f"Now playing: {prev_item.format_display()}")

        elif user_choice == "4":
            repeat_status = queue_system.toggle_repeat()
            print(f"Repeat: {'ON' if repeat_status else 'OFF'}")

        elif user_choice == "5":
            if queue_system.is_shuffled():
                queue_system.unshuffle()
                print("Shuffle turned OFF")
            else:
                queue_system.shuffle()
                print("Shuffle turned ON")

        elif user_choice == "6":
            confirmation = input("Clear queue? (y/n): ")
            if confirmation.lower() == 'y':
                queue_system.clear()
                print("Queue cleared!")

        elif user_choice == "7":
            break

def main():
    print("Welcome to Listen to the Music!")

    while True:
        show_main_menu()
        user_input = input("Enter your choice: ")

        if user_input == "1":
            process_library_actions()
        elif user_input == "2":
            process_playlist_actions()
        elif user_input == "3":
            process_queue_actions()
        elif user_input == "4":
            print("Thanks for using Listen to the Music!")
            break
        else:
            print("Invalid choice!")

if __name__ == '__main__':
    main()
