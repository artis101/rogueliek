import random
from typing import List
from src.rogueliek.room import Room


class Dungeon:
    def __init__(
        self, width: int, height: int, max_rooms: int, seed: int | None = None
    ):
        self.width = width
        self.height = height
        self.max_rooms = max_rooms
        self.seed = seed if seed is not None else random.randint(0, 2**32 - 1)
        self.rng = random.Random(self.seed)
        self.rooms: List[Room] = []
        self.grid: List[List[int]] = [[0 for _ in range(width)] for _ in range(height)]

        self._generate_dungeon()

    def _generate_dungeon(self):
        attempts = 0
        max_attempts = self.max_rooms * 3  # Allow for some failed placements

        while len(self.rooms) < self.max_rooms and attempts < max_attempts:
            room_width = self.rng.randint(10, min(20, self.width // 2))
            room_height = self.rng.randint(7, min(10, self.height // 2))

            x = self.rng.randint(0, self.width - room_width)
            y = self.rng.randint(0, self.height - room_height)

            if self._can_place_room(x, y, room_width, room_height):
                room_seed = self.rng.randint(0, 2**32 - 1)
                is_dead_end = len(self.rooms) == self.max_rooms - 1

                new_room = Room(
                    room_width, room_height, seed=room_seed, is_dead_end=is_dead_end
                )

                self.rooms.append(new_room)
                self._place_room(x, y, room_width, room_height)

            attempts += 1

    def _can_place_room(self, x: int, y: int, width: int, height: int) -> bool:
        if x + width > self.width or y + height > self.height:
            return False

        for i in range(y - 1, y + height + 1):
            for j in range(x - 1, x + width + 1):
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.grid[i][j] != 0:
                        return False
        return True

    def _place_room(self, x: int, y: int, width: int, height: int):
        for i in range(y, y + height):
            for j in range(x, x + width):
                self.grid[i][j] = len(self.rooms)  # Mark with room number

    def get_room_at(self, x: int, y: int) -> Room | None:
        room_index = self.grid[y][x]
        return self.rooms[room_index - 1] if room_index > 0 else None

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                room_index = self.grid[y][x]
                if room_index == 0:
                    print(" ", end="")
                else:
                    room = self.rooms[room_index - 1]
                    local_x = x - self.grid[y].index(room_index)
                    local_y = y - next(
                        i for i, row in enumerate(self.grid) if room_index in row
                    )
                    print(room.tiles[local_y][local_x].char, end="")
            print()
