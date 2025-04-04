import numpy as np  # type: ignore
from tcod.console import Console
from tcod.ecs import Registry

import game.ecs.components as components
import game.ecs.tags as tags
from game.core import tile_types


class GameMap:
    def __init__(self, width: int, height: int, entities: Registry):
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")
        self.entities = entities

        self.visible = np.full((width, height), fill_value=False, order="F")
        self.explored = np.full((width, height), fill_value=False, order="F")

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
       """
       Renders the map.

       If a tile is in the "visible" array, then draw it with the "light" graphics.
       If it isn't, but it's in the "explored" array, then draw it with the "dark" graphics.
       Otherwise, the default is "SHROUD".
       """
       console.tiles_rgb[0:self.width, 0:self.height] = np.select(
           condlist=[self.visible, self.explored],
           choicelist=[self.tiles["light"], self.tiles["dark"]],
           default=tile_types.SHROUD,
       )

       for entity in self.entities.Q.all_of(components=(components.Position, components.Graphic)):
           position = entity.components[components.Position]
           # Only print entities that are in the FOV
           if self.game_map.visible[position.x, position.y]:
               graphic = entity.components[components.Graphic]
               console.print(position.x, position.y, graphic.char, graphic.fg, graphic.bg)

