from src.rogueliek.dungeon import Dungeon
from src.rogueliek.room import Room

if __name__ == "__main__":
    room = Room(20, 10, seed=42)
    room.render(show_path_to_exit=True)

    dungeon = Dungeon(80, 40, max_rooms=10)
    dungeon.render()
