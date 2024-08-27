from rogueliek.types import TileType


class Tile:
    def __init__(self, type: TileType, char: str, walkable: bool, description: str):
        self.type = type
        self.char = char
        self.walkable = walkable
        self.description = description
