import pytest
from ..dungeon import Dungeon, DungeonConfig, Room, RoomType, EntityType


@pytest.fixture
def dungeon():
    config = DungeonConfig(
        width=80,
        height=40,
        num_rooms=15,
        room_min_size=5,
        room_max_size=12,
        room_type_weights={
            RoomType.NORMAL: 1,
            RoomType.TREASURE: 0,
            RoomType.TRAP: 0,
            RoomType.BOSS: 0,
        },
        corridor_windingness=0.2,
        entity_counts={
            EntityType.PLAYER: 1,
            EntityType.MONSTER: 0,
            EntityType.ITEM: 0,
            EntityType.NPC: 0,
        },
    )
    return Dungeon(config)


# generate the full dungeon before running the tests
def test_generate(dungeon):
    dungeon.generate()
    assert len(dungeon.rooms) <= 15
    assert len(dungeon.entities) == 1  # Player entity


def test_entry_door_top_edge(dungeon):
    entry_x, entry_y = 5, 1  # Top edge
    dungeon.generate()
    room = Room(0, 0, 10, 10, RoomType.NORMAL)
    dungeon.generate_room(room, entry_x, entry_y)
    room.print()
    import pdb

    pdb.set_trace()
    result = dungeon._get_entry_door_point(room, entry_x, entry_y)
    assert result == (5, 0)  # One step up


# def test_entry_door_left_edge(dungeon):
#     room = Room(10, 10, 20, 15, RoomType.NORMAL)
#     entry_x, entry_y = 10, 17  # Left edge
#     result = dungeon._get_entry_door_point(room, entry_x, entry_y)
#     assert result == (1, 7)  # One step to the right
#
#
# def test_entry_door_right_edge(dungeon):
#     room = Room(10, 10, 20, 15, RoomType.NORMAL)
#     entry_x, entry_y = 29, 17  # Right edge
#     result = dungeon._get_entry_door_point(room, entry_x, entry_y)
#     assert result == (18, 7)  # One step to the left
#
#
# def test_entry_door_bottom_edge(dungeon):
#     room = Room(10, 10, 20, 15, RoomType.NORMAL)
#     entry_x, entry_y = 20, 24  # Bottom edge
#     result = dungeon._get_entry_door_point(room, entry_x, entry_y)
#     assert result == (10, 13)  # One step up
#
#
# def test_entry_door_corner(dungeon):
#     room = Room(10, 10, 20, 15, RoomType.NORMAL)
#     entry_x, entry_y = 10, 10  # Top-left corner
#     result = dungeon._get_entry_door_point(room, entry_x, entry_y)
#     assert result in [(1, 0), (0, 1)]  # Either one step right or one step down
#
#
# def test_entry_door_inside_room(dungeon):
#     room = Room(10, 10, 20, 15, RoomType.NORMAL)
#     entry_x, entry_y = 15, 15  # Inside the room
#     result = dungeon._get_entry_door_point(room, entry_x, entry_y)
#     assert result == (5, 5)  # Should return the same point relative to room
