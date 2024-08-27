import math
from typing import Tuple, List, Callable, Dict


def euclidean_distance(tile1: Tuple[int, int], tile2: Tuple[int, int]) -> float:
    return math.sqrt((tile1[0] - tile2[0]) ** 2 + (tile1[1] - tile2[1]) ** 2)


def astar_between_tiles(
    start: Tuple[int, int],
    end: Tuple[int, int],
    get_tile_neighbors: Callable[[Tuple[int, int]], List[Tuple[int, int]]],
) -> List[Tuple[int, int]]:
    open_set = {start}
    came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
    g_score: Dict[Tuple[int, int], float] = {start: 0}
    f_score: Dict[Tuple[int, int], float] = {start: euclidean_distance(start, end)}

    while open_set:
        current = min(open_set, key=lambda tile: f_score.get(tile, math.inf))
        if current == end:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]

        open_set.remove(current)
        for neighbor in get_tile_neighbors(current):
            # Assuming get_tile_neighbors already filters out non-walkable tiles
            movement_cost = euclidean_distance(current, neighbor)
            tentative_g_score = g_score[current] + movement_cost

            if tentative_g_score < g_score.get(neighbor, math.inf):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + euclidean_distance(
                    neighbor, end
                )
                if neighbor not in open_set:
                    open_set.add(neighbor)

    return []  # No path found

