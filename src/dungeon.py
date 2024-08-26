import random
from typing import List, Tuple
from .tile import Tile
from .room import Room
from .entity import Entity
from .types import TileType, RoomType, EntityType
from .config import DungeonConfig


class Dungeon:
    def __init__(self, config: DungeonConfig):
        self.config = config
        self.tiles: List[List[Tile]] = []
        self.rooms: List[Room] = []
        self.entities: List[Entity] = []
        self.tile_types = {
            TileType.WALL: Tile(TileType.WALL, "#", False, "A solid wall"),
            TileType.FLOOR: Tile(TileType.FLOOR, ".", True, "A stone floor"),
            TileType.DOOR: Tile(TileType.DOOR, "+", True, "A wooden door"),
            TileType.TREASURE: Tile(TileType.TREASURE, "$", True, "A glittering floor"),
            TileType.TRAP: Tile(TileType.TRAP, "^", True, "A suspicious floor"),
            TileType.WATER: Tile(TileType.WATER, "~", False, "A pool of water"),
            TileType.ENTRY: Tile(TileType.ENTRY, "<", True, "The dungeon entrance"),
        }

    def generate(self):
        self._initialize_tiles()
        self._generate_rooms()
        self._connect_rooms()
        self._place_doors()
        self._place_entities()

    def _initialize_tiles(self):
        self.tiles = [
            [self.tile_types[TileType.WALL] for _ in range(self.config.width)]
            for _ in range(self.config.height)
        ]

    def _generate_rooms(self):
        for _ in range(self.config.num_rooms):
            width = random.randint(self.config.room_min_size, self.config.room_max_size)
            height = random.randint(
                self.config.room_min_size, self.config.room_max_size
            )
            x = random.randint(1, self.config.width - width - 1)
            y = random.randint(1, self.config.height - height - 1)

            if not self._intersects(x, y, width, height):
                room_type = random.choices(
                    list(RoomType),
                    weights=[
                        self.config.room_type_weights.get(rt, 1) for rt in RoomType
                    ],
                )[0]
                new_room = Room(x, y, width, height, room_type)
                self._carve_room(new_room)
                self.rooms.append(new_room)

    def _intersects(self, x: int, y: int, width: int, height: int) -> bool:
        return any(
            self._rooms_intersect(Room(x, y, width, height, RoomType.NORMAL), room)
            for room in self.rooms
        )

    def _rooms_intersect(self, room1: Room, room2: Room) -> bool:
        return (
            room1.x < room2.x + room2.width
            and room1.x + room1.width > room2.x
            and room1.y < room2.y + room2.height
            and room1.y + room1.height > room2.y
        )

    def _carve_room(self, room: Room):
        for y in range(room.y, room.y + room.height):
            for x in range(room.x, room.x + room.width):
                if room.type == RoomType.NORMAL:
                    self.tiles[y][x] = self.tile_types[TileType.FLOOR]
                elif room.type == RoomType.TREASURE:
                    self.tiles[y][x] = self.tile_types[TileType.TREASURE]
                elif room.type == RoomType.TRAP:
                    self.tiles[y][x] = self.tile_types[TileType.TRAP]

    def _connect_rooms(self):
        for i in range(len(self.rooms) - 1):
            start = self._get_room_center(self.rooms[i])
            end = self._get_room_center(self.rooms[i + 1])
            self._create_corridor(start, end)

    def _get_room_center(self, room: Room) -> Tuple[int, int]:
        return (room.x + room.width // 2, room.y + room.height // 2)

    def _create_corridor(self, start: Tuple[int, int], end: Tuple[int, int]):
        x, y = start
        while (x, y) != end:
            if random.random() > self.config.corridor_windingness:
                x += 1 if x < end[0] else -1 if x > end[0] else 0
            else:
                y += 1 if y < end[1] else -1 if y > end[1] else 0
            if 0 <= x < self.config.width and 0 <= y < self.config.height:
                self.tiles[y][x] = self.tile_types[TileType.FLOOR]

    def _place_doors(self):
        for room in self.rooms:
            for x in range(room.x, room.x + room.width):
                if self._is_door_candidate(x, room.y - 1) and random.random() < 0.5:
                    self.tiles[room.y - 1][x] = self.tile_types[TileType.DOOR]
                    room.exit_points.append((x, room.y - 1))
                if (
                    self._is_door_candidate(x, room.y + room.height)
                    and random.random() < 0.5
                ):
                    self.tiles[room.y + room.height][x] = self.tile_types[TileType.DOOR]
                    room.exit_points.append((x, room.y + room.height))
            for y in range(room.y, room.y + room.height):
                if self._is_door_candidate(room.x - 1, y) and random.random() < 0.5:
                    self.tiles[y][room.x - 1] = self.tile_types[TileType.DOOR]
                    room.exit_points.append((room.x - 1, y))
                if (
                    self._is_door_candidate(room.x + room.width, y)
                    and random.random() < 0.5
                ):
                    self.tiles[y][room.x + room.width] = self.tile_types[TileType.DOOR]
                    room.exit_points.append((room.x + room.width, y))

    def _is_door_candidate(self, x: int, y: int) -> bool:
        if not (0 <= x < self.config.width and 0 <= y < self.config.height):
            return False
        return (
            self.tiles[y][x].type == TileType.WALL
            and sum(
                1
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                if 0 <= x + dx < self.config.width
                and 0 <= y + dy < self.config.height
                and self.tiles[y + dy][x + dx].type == TileType.FLOOR
            )
            >= 1
        )

    def _place_entities(self):
        for entity_type, count in self.config.entity_counts.items():
            for _ in range(count):
                room = random.choice(self.rooms)
                x = random.randint(room.x, room.x + room.width - 1)
                y = random.randint(room.y, room.y + room.height - 1)
                char = (
                    "@"
                    if entity_type == EntityType.PLAYER
                    else "M"
                    if entity_type == EntityType.MONSTER
                    else "I"
                    if entity_type == EntityType.ITEM
                    else "N"
                )
                entity = Entity(entity_type, char, x, y)
                self.entities.append(entity)
                room.entities.append(entity)

    def generate_room(self, room: Room, entry_x: int, entry_y: int):
        room.entry_point = (entry_x, entry_y)
        room.tiles = [
            [self.tile_types[TileType.WALL] for _ in range(room.width)]
            for _ in range(room.height)
        ]

        # Set entry point as a door
        room.tiles[entry_y - room.y][entry_x - room.x] = self.tile_types[TileType.DOOR]

        # Generate room layout
        self._generate_room_layout(room)

        # Place features and entities
        self._place_room_features(room)
        self._place_room_entities(room)

        # Place exit points
        self._place_room_exits(room)

        # Place a door behind the entry point
        behind_x, behind_y = self._get_entry_door_point(room, entry_x, entry_y)
        if 0 <= behind_x < room.width and 0 <= behind_y < room.height:
            room.tiles[behind_y][behind_x] = self.tile_types[TileType.DOOR]

        # Place player at the entry point
        player_entity = next(
            (e for e in room.entities if e.type == EntityType.PLAYER), None
        )
        if player_entity:
            player_entity.x, player_entity.y = entry_x, entry_y
        else:
            room.entities.append(Entity(EntityType.PLAYER, "@", entry_x, entry_y))

        return room.seed  # Return the seed used for this room

    def _generate_room_layout(self, room: Room):
        # Fill the room with floor tiles, leaving a border of walls
        for y in range(1, room.height - 1):
            for x in range(1, room.width - 1):
                room.tiles[y][x] = self.tile_types[TileType.FLOOR]

        # Optionally, add some internal walls or pillars
        self._add_internal_features(room)

    def _add_internal_features(self, room: Room):
        # Add some internal walls or pillars with low probability
        for y in range(2, room.height - 2):
            for x in range(2, room.width - 2):
                if room.rng.random() < 0.05:  # 5% chance for each tile
                    room.tiles[y][x] = self.tile_types[TileType.WALL]

    def _place_room_features(self, room: Room):
        feature_count = room.rng.randint(1, 3)
        features = [TileType.TRAP, TileType.TREASURE, TileType.WATER]
        for _ in range(feature_count):
            feature = room.rng.choice(features)
            x, y = self._find_empty_tile(room)
            room.tiles[y][x] = self.tile_types[feature]

    def _place_room_entities(self, room: Room):
        entity_count = room.rng.randint(1, 4)
        for _ in range(entity_count):
            entity_type = room.rng.choice(
                [EntityType.MONSTER, EntityType.ITEM, EntityType.NPC]
            )
            x, y = self._find_empty_tile(room)
            char = (
                "M"
                if entity_type == EntityType.MONSTER
                else "I"
                if entity_type == EntityType.ITEM
                else "N"
            )
            entity = Entity(entity_type, char, x + room.x, y + room.y)
            room.entities.append(entity)

    def _find_empty_tile(self, room: Room) -> Tuple[int, int]:
        while True:
            x = room.rng.randint(1, room.width - 2)
            y = room.rng.randint(1, room.height - 2)
            if room.tiles[y][x].type == TileType.FLOOR:
                return x, y

    def _place_room_exits(self, room: Room):
        num_exits = room.rng.randint(1, 3)
        possible_exits = []

        # Only place exits on the edges of the room
        for x in range(room.width):
            possible_exits.extend([(x, 0), (x, room.height - 1)])
        for y in range(1, room.height - 1):
            possible_exits.extend([(0, y), (room.width - 1, y)])

        exits = room.rng.sample(possible_exits, min(num_exits, len(possible_exits)))
        for x, y in exits:
            if (x + room.x, y + room.y) != room.entry_point:
                room.tiles[y][x] = self.tile_types[TileType.DOOR]
                room.exit_points.append((x + room.x, y + room.y))

    def _get_entry_door_point(
        self, room: Room, entry_x: int, entry_y: int
    ) -> Tuple[int, int]:
        dx = entry_x - room.x
        dy = entry_y - room.y

        if dx == 0:
            return dx, dy - 1 if dy > 0 else dy + 1
        elif dx == room.width - 1:
            return dx, dy - 1 if dy > 0 else dy + 1
        elif dy == 1:
            return dx - 1 if dx > 0 else dx + 1, dy
        elif dy == room.height - 1:
            return dx - 1 if dx > 0 else dx + 1, dy
        else:
            # If entry point is not on the edge, place the door in a valid direction
            for direction in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
                new_x, new_y = dx + direction[0], dy + direction[1]
                if 0 <= new_x < room.width and 0 <= new_y < room.height:
                    return new_x, new_y

            # If no valid direction found, return the original entry point
            return dx, dy

    def explore_dungeon(self):
        current_room = random.choice(self.rooms)
        visited_rooms = set()

        while len(visited_rooms) < len(self.rooms):
            if current_room not in visited_rooms:
                print(f"\nEntering room at ({current_room.x}, {current_room.y}):")
                entry_x, entry_y = current_room.x, current_room.y
                if visited_rooms:  # Not the first room
                    # Find a suitable entry point (door) for the new room
                    for x in range(current_room.width):
                        for y in range(current_room.height):
                            if (
                                self.tiles[current_room.y + y][current_room.x + x].type
                                == TileType.DOOR
                            ):
                                entry_x, entry_y = (
                                    current_room.x + x,
                                    current_room.y + y,
                                )
                                break
                        if entry_x != current_room.x or entry_y != current_room.y:
                            break

                self.generate_room(current_room, entry_x, entry_y)
                room_map = [[tile.char for tile in row] for row in current_room.tiles]
                for entity in current_room.entities:
                    room_map[entity.y - current_room.y][entity.x - current_room.x] = (
                        entity.char
                    )
                print("\n".join("".join(row) for row in room_map))
                visited_rooms.add(current_room)

            if current_room.exit_points:
                next_exit = random.choice(current_room.exit_points)
                next_room = next(
                    (
                        room
                        for room in self.rooms
                        if room != current_room
                        and room.x <= next_exit[0] < room.x + room.width
                        and room.y <= next_exit[1] < room.y + room.height
                    ),
                    None,
                )
                if next_room:
                    print(f"Moving to room at ({next_room.x}, {next_room.y})")
                    current_room = next_room
                else:
                    print("Dead end. Backtracking...")
                    current_room = random.choice(list(visited_rooms))
            else:
                print("No exits. Backtracking...")
                current_room = random.choice(list(visited_rooms))

    def __str__(self):
        dungeon_map = [[tile.char for tile in row] for row in self.tiles]
        for entity in self.entities:
            dungeon_map[entity.y][entity.x] = entity.char

        return "\n".join("".join(row) for row in dungeon_map)
