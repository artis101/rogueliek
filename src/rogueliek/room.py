import random

from typing import Tuple, List

from src.rogueliek.tiles_registry import TR
from src.rogueliek.types import TileType, Side
from src.rogueliek.distance import euclidean_distance, astar_between_tiles


class Room:
    CARDINAL_DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    DIAGONAL_DIRECTIONS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    ALL_DIRECTIONS = CARDINAL_DIRECTIONS + DIAGONAL_DIRECTIONS

    _iterations: int = 0

    def __init__(
        self,
        width: int,
        height: int,
        seed=None,
        prev_room: "Room | None" = None,
        next_room: "Room | None" = None,
        is_dead_end: bool = False,
        bulk: bool = False,
    ):
        self.width = width
        self.height = height
        self.seed = seed if seed is not None else random.randint(0, 2**32 - 1)
        self.rng = random.Random(self.seed)
        self.prev_room = prev_room
        self.next_room = next_room
        self.is_dead_end = is_dead_end
        self.tiles = []
        self.entry_position: Tuple[int, int] | None = None
        self.exit_position: Tuple[int, int] | None = None

        if not bulk:
            self._init()

    def __str__(self):
        return f"Room(width={self.width}, height={self.height}, seed={self.seed}"

    def debug(self):
        return f"Room(width={self.width}, height={self.height}, seed={self.seed}, prev_room={self.prev_room}, next_room={self.next_room}, is_dead_end={self.is_dead_end})"

    def _init(self):
        # Generate the room by generating the floors and walls first
        self._generate_floor()
        self._generate_walls()
        # All rooms have an entry door/point
        self._generate_entry_point()

        if not self.is_dead_end:
            self._generate_exit_point()

    def _generate_floor(self):
        self.tiles = [
            [TR[TileType.STONE_FLOOR] for _ in range(self.width)]
            for _ in range(self.height)
        ]

    def _generate_walls(self):
        for x in range(self.width):
            for y in range(self.height):
                if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                    self.tiles[y][x] = TR[TileType.STONE_WALL]

    def _generate_entry_point(self, use_side: Side | None = None):
        side = use_side or self.rng.choice(
            [
                Side.LEFT,
                Side.BOTTOM,
                Side.TOP,
                Side.RIGHT,
            ]
        )

        if side == Side.TOP:
            x = self.rng.randint(1, self.width - 2)
            y = 0
        elif side == Side.BOTTOM:
            x = self.rng.randint(1, self.width - 2)
            y = self.height - 1
        elif side == Side.LEFT:
            x = 0
            y = self.rng.randint(1, self.height - 2)
        elif side == Side.RIGHT:
            x = self.width - 1
            y = self.rng.randint(1, self.height - 2)
        else:
            raise ValueError(f"Invalid side: {side}")

        entry_tile_type = (
            TR[TileType.WOODEN_DOOR] if self.prev_room else TR[TileType.ENTRY]
        )

        self.tiles[y][x] = entry_tile_type
        self.entry_position = self._find_adjacent_spot((y, x))

    def _generate_exit_point(self, use_side: Side | None = None):
        self._iterations += 1
        side = use_side or self.rng.choice(
            [
                Side.LEFT,
                Side.BOTTOM,
                Side.TOP,
                Side.RIGHT,
            ]
        )
        if side == Side.TOP:
            x = self.rng.randint(1, self.width - 2)
            y = 0
        elif side == Side.BOTTOM:
            x = self.rng.randint(1, self.width - 2)
            y = self.height - 1
        elif side == Side.LEFT:
            x = 0
            y = self.rng.randint(1, self.height - 2)
        elif side == Side.RIGHT:
            x = self.width - 1
            y = self.rng.randint(1, self.height - 2)
        else:
            raise ValueError(f"Invalid side: {side}")

        if (
            not use_side
            and euclidean_distance((x, y), self.entry_position) < self.width // 2  # type: ignore
        ):
            opposite_side = {
                Side.TOP: Side.BOTTOM,
                Side.BOTTOM: Side.TOP,
                Side.LEFT: Side.RIGHT,
                Side.RIGHT: Side.LEFT,
            }[side]
            self._generate_exit_point(use_side=opposite_side)
            return

        exit_tile_type = (
            TR[TileType.WOODEN_DOOR] if self.next_room else TR[TileType.EXIT]
        )

        self.tiles[y][x] = exit_tile_type
        self.exit_position = self._find_adjacent_spot((y, x))

    def _find_adjacent_spot(self, position: Tuple[int, int]) -> Tuple[int, int] | None:
        x, y = position
        for dx, dy in [
            (0, -1),
            (0, 1),
            (-1, 0),
            (1, 0),
        ]:
            if self.is_tile_walkable((x + dx, y + dy)):
                return x + dx, y + dy

    def is_tile_walkable(self, position: Tuple[int, int]) -> bool:
        y, x = position
        return (
            0 < x < self.width - 1
            and 0 < y < self.height - 1
            and self.tiles[y][x].walkable
        )

    def get_tile_neighbors(
        self, position: Tuple[int, int], include_diagonals: bool = False
    ) -> List[Tuple[int, int]]:
        y, x = position  # Note the order change
        directions = (
            self.ALL_DIRECTIONS if include_diagonals else self.CARDINAL_DIRECTIONS
        )
        return [
            (y + dy, x + dx)  # Note the order change
            for dx, dy in directions
            if self.is_tile_walkable((y + dy, x + dx))
        ]

    # This method is used to print the room in the console
    # It is not used in the game itself but is useful for debugging
    # and testing. It always prints a standalone room.
    def render(self, show_path_to_exit: bool = False):
        print(f"Room seed: {self.seed} (iterations: {self._iterations})")

        if show_path_to_exit and self.is_dead_end:
            raise ValueError("Cannot show path to exit in a dead end room")

        path = None
        if show_path_to_exit:
            path = astar_between_tiles(
                self.entry_position,  # type: ignore
                self.exit_position,  # type: ignore
                self.get_tile_neighbors,
            )

        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if show_path_to_exit and path and (y, x) in path:
                    print("\033[92m" + tile.char + "\033[0m", end="")
                else:
                    print(tile.char, end="")
            print()
