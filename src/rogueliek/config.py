from typing import Dict
from rogueliek.types import RoomType, EntityType


class DungeonConfig:
    def __init__(
        self,
        width: int,
        height: int,
        num_rooms: int,
        room_min_size: int,
        room_max_size: int,
        room_type_weights: Dict[RoomType, float],
        corridor_windingness: float,
        entity_counts: Dict[EntityType, int],
    ):
        self.width = width
        self.height = height
        self.num_rooms = num_rooms
        self.room_min_size = room_min_size
        self.room_max_size = room_max_size
        self.room_type_weights = room_type_weights
        self.corridor_windingness = corridor_windingness
        self.entity_counts = entity_counts
