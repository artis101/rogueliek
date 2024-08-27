from rogueliek.types import EntityType


class Entity:
    def __init__(self, type: EntityType, char: str, x: int, y: int):
        self.type = type
        self.char = char
        self.x = x
        self.y = y
