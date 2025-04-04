from typing import Set, Iterable, Any




from tcod.context import Context
from tcod.console import Console
from tcod.ecs import Registry

from game.core.game_map import GameMap
from game.core.input_handlers import EventHandler
from game.ecs.components import Position, Graphic
from game.ecs.tags import IsPlayer


class Engine:
    def __init__(self, entities: Registry, event_handler: EventHandler, game_map: GameMap):
        self.entities = entities
        self.event_handler = event_handler
        self.game_map = game_map

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)
            if action is None:
                continue

            for player in self.entities.Q.all_of(tags=[IsPlayer]):
                action.perform(self, player)


    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        for entity in self.entities.Q.all_of(components=(Position, Graphic)):
            position = entity.components[Position]
            if not (0 <= position.x < console.width and 0 <= position.y < console.height):
                continue
            graphic = entity.components[Graphic]

            console.print(x=position.x, y=position.y, string=graphic.char, fg=graphic.fg)

        context.present(console)

        console.clear()

class camera:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def screen_to_map(self, x: int, y: int) -> tuple[int, int]:
        return (x - self.x, y - self.y)

    def map_to_screen(self, x: int, y: int) -> tuple[int, int]:
        return (x + self.x, y + self.y)