from src.rogueliek.dungeon import Dungeon
from src.rogueliek.room import Room

if __name__ == "__main__":
    room = Room(20, 10, seed=420)
    room.render(render_player=True)

    # dungeon = Dungeon(80, 40, max_rooms=10, seed=3744154005)
    # dungeon.render()
