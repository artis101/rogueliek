from src.rogueliek.types import TileType
from src.rogueliek.tile import Tile

TR = {
    TileType.ENTRY: Tile(TileType.ENTRY, "E", False, "The entry point to the dungeon"),
    TileType.STONE_WALL: Tile(TileType.STONE_WALL, "#", False, "A solid stone wall"),
    TileType.STONE_FLOOR: Tile(TileType.STONE_FLOOR, ".", True, "A stone floor"),
    TileType.WOODEN_DOOR: Tile(TileType.WOODEN_DOOR, "+", True, "A wooden door"),
    TileType.EXIT: Tile(TileType.EXIT, "X", False, "The exit point"),
    TileType.PLAYER: Tile(TileType.PLAYER, "@", True, "The player (you)"),
}
