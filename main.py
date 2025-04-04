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
    tileset = tcod.tileset.load_tilesheet(
        "assets/Haberdash_curses_12x12.png", 16, 16, tcod.tileset.CHARMAP_CP437
    )

    event_handler = EventHandler()

    world = tcod.ecs.Registry()

    player = world[object()]
    player.components[Position] = Position(int(map_width/2), int(map_height/2))
    player.components[Graphic] = Graphic("@", (255,255,255))
    player.tags |= {IsPlayer, IsActor}

    npc = world[object()]
    npc.components[Position] = Position(int(map_width/2)-1, int(map_height/2)-1)
    npc.components[Graphic] = Graphic("N", (255,255,255))
    npc.tags |= {IsActor}

    CA = CellularAutomata()
    game_map = CA.generate_dungeon(map_width,map_height)

    engine = Engine(world, event_handler, game_map)

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="RogueWorld",
        vsync=True,
    ) as context:
        root_console = tcod.Console(80, 50, order="F")
        while True:
            engine.render(console=root_console, context=context)

            events = tcod.event.wait()

            engine.handle_events(events)


if __name__ == "__main__":
    main()



