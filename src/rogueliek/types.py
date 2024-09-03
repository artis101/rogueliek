from enum import Enum


class TileType(Enum):
    # Environment tiles
    STONE_WALL = 10
    STONE_FLOOR = 20
    WOODEN_DOOR = 30
    # Special tiles (e.g. entry point) have higher values
    ENTRY = 1001  # Entry point to the dungeon
    PLAYER = 1337  # Player
    EXIT = 9999  # Exit from the dungeon. You beat the game!


class Side(Enum):
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"
