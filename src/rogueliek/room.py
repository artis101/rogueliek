import random
from typing import List, Optional, Tuple
from rogueliek.types import RoomType
from rogueliek.tile import Tile
from rogueliek.entity import Entity
from rogueliek.config import DungeonConfig


class Room:
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        room_type: RoomType,
        config: DungeonConfig,
        seed: Optional[int] = None,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = room_type
        self.config = config
        self.tiles: List[List[Tile]] = []
        self.entities: List[Entity] = []
        self.entry_point: Optional[Tuple[int, int]] = None
        self.exit_points: List[Tuple[int, int]] = []
        self.seed = seed if seed is not None else random.randint(0, 2**32 - 1)
        self.rng = random.Random(self.seed)

    def print(self):
        room_map = [[tile.char for tile in row] for row in self.tiles]
        for entity in self.entities:
            room_map[entity.y - self.y][entity.x - self.x] = entity.char
        print("\n".join("".join(row) for row in room_map))
