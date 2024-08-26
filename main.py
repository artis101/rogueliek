from src.dungeon import Dungeon, DungeonConfig
from src.room import Room
from src.types import RoomType, EntityType


if __name__ == "__main__":
    config = DungeonConfig(
        width=80,
        height=40,
        num_rooms=15,
        room_min_size=5,
        room_max_size=12,
        room_type_weights={
            RoomType.NORMAL: 0.6,
            RoomType.TREASURE: 0.2,
            RoomType.TRAP: 0.1,
            RoomType.BOSS: 0.05,
        },
        corridor_windingness=0.2,
        entity_counts={
            EntityType.PLAYER: 1,
            EntityType.MONSTER: 10,
            EntityType.ITEM: 5,
            EntityType.NPC: 2,
        },
    )

    # Generate the full dungeon
    dungeon = Dungeon(config)
    dungeon.generate()

    # Now let's demonstrate generating a single room with a specific entry point and seed
    sample_room = Room(0, 0, 20, 15, RoomType.NORMAL, seed=42)  # Use seed 42
    room_seed = dungeon.generate_room(sample_room, 7, 1)

    print("Single Room (Seed:", room_seed, "):")
    sample_room.print()

    print(f"\nRoom entry point: {sample_room.entry_point}")
    print(f"Room exit points: {sample_room.exit_points}")

    # Generate the same room again with the same seed
    print("\nRegenerating the same room with seed:", room_seed)
    same_room = Room(0, 0, 20, 15, RoomType.NORMAL, seed=room_seed)
    dungeon.generate_room(same_room, 7, 1)

    print("Regenerated Room:")
    same_room.print()

    print(f"\nRoom entry point: {same_room.entry_point}")
    print(f"Room exit points: {same_room.exit_points}")
