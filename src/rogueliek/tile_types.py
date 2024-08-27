from rogueliek.tile import Tile
from rogueliek.types import TileType

TILE_TYPES = {
    TileType.WALL: Tile(TileType.WALL, "#", False, "A solid wall"),
    TileType.FLOOR: Tile(TileType.FLOOR, ".", True, "A stone floor"),
    TileType.DOOR: Tile(TileType.DOOR, "+", True, "A wooden door"),
    TileType.TREASURE: Tile(TileType.TREASURE, "$", True, "A glittering floor"),
    TileType.TRAP: Tile(TileType.TRAP, "^", True, "A suspicious floor"),
    TileType.WATER: Tile(TileType.WATER, "~", False, "A pool of water"),
    TileType.ENTRY: Tile(TileType.ENTRY, "<", True, "The dungeon entrance"),
}
