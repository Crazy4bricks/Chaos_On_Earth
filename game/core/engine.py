from typing import Set, Iterable, Any




from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov
from tcod.ecs import Registry

from game.core.game_map import GameMap
from game.core.input_handlers import EventHandler
from game.ecs.components import Position, Graphic
from game.ecs.tags import IsPlayer


class Engine:
    def __init__(self, event_handler: EventHandler, game_map: GameMap):
        self.event_handler = event_handler
        self.game_map = game_map
        self.update_fov()

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)
            if action is None:
                continue

            for player in self.entities.Q.all_of(tags=[IsPlayer]):
                action.perform(self, player)

            self.update_fov()


    def update_fov(self):
        """Recompute the visible area based on the players point of view."""
        for player in self.entities.Q.all_of(tags=[IsPlayer]):
            position = player.components[Position]
            self.game_map.visible[:] = compute_fov(
                self.game_map.tiles["transparent"],
                (position.x, position.y),
                radius=8,
            )
            # If a tile is "visible" it should be added to "explored".
            self.game_map.explored |= self.game_map.visible


    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)


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