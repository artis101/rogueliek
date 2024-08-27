from src.rogueliek.room import Room

if __name__ == "__main__":
    room = Room(20, 10, seed=42)
    room.render(show_path_to_exit=True)
