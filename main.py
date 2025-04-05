import tcod

import tcod.ecs
from game.core.engine import Engine
from game.procgen.basic import generate_dungeon
from game.procgen.cell_auto import CellularAutomata
from game.core.input_handlers import EventHandler
from game.ecs.tags import IsItem, IsPlayer, IsActor
from game.ecs.components import Graphic, Position

def main() -> None:
    screen_width = 80
    screen_height = 60

    map_width = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    max_monsters_per_room = 3

    tileset = tcod.tileset.load_tilesheet(
        "assets/Haberdash_curses_12x12.png", 16, 16, tcod.tileset.CHARMAP_CP437
    )

    event_handler = EventHandler()

    world = tcod.ecs.Registry()

    player = world[object()]
    player.components[Position] = Position(int(map_width/2), int(map_height/2))
    player.components[Graphic] = Graphic("@", (255,255,255))
    player.tags |= {IsPlayer, IsActor}

    game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        max_monsters_per_room=max_monsters_per_room,
        entities=world,
    )

    engine = Engine(event_handler, game_map)

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="RogueWorld",
        vsync=True,
    ) as context:
        root_console = tcod.console.Console(80, 50, order="F")
        while True:
            engine.render(console=root_console, context=context)

            events = tcod.event.wait()

            engine.handle_events(events)


if __name__ == "__main__":
    main()



