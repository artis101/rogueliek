from enum import Enum


class TileType(Enum):
    WALL = 0
    FLOOR = 1
    DOOR = 2
    TREASURE = 3
    TRAP = 4
    WATER = 5
    ENTRY = 6


class RoomType(Enum):
    NORMAL = 0
    TREASURE = 1
    TRAP = 2
    BOSS = 3


class EntityType(Enum):
    PLAYER = 0
    MONSTER = 1
    ITEM = 2
    NPC = 3
