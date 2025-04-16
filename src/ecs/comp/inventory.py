from __future__ import annotations

from typing import TYPE_CHECKING, List

from src.ecs.comp.base_component import BaseComponent

if TYPE_CHECKING:
    from src.entity import Actor, Item


from typing import Final, Self, Optional

import attrs
import self
import tcod.ecs.callbacks
from tcod.ecs import Entity


class Inventory(BaseComponent):
    parent: Actor

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.items: List[Item] = []

    def drop(self, item: Item) -> None:
        """
        Removes an item from the inventory and restores it to the src map, at the player's current location.
        """
        self.items.remove(item)
        item.place(self.parent.x, self.parent.y, self.gamemap)

        self.engine.message_log.add_message(f"You dropped the {item.name}.")

@attrs.define(frozen=True)
class Potion():
    """Entity that is a potion."""
    heal_amount: int

@attrs.define(frozen=True)
class InBackpack():
    owner: Entity
