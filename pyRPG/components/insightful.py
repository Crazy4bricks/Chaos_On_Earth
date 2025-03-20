from __future__ import annotations

from typing import List, TYPE_CHECKING

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from core.entity import Entity, Actor, Item
    
class Insightful(BaseComponent)
    parent: Entity
    
    def __init__(
        insight: Optional[int] = 0, #The amount of insight an entity has.
        name: Optional[str] = "", #The true name of the entity.
        description: Optional[str] = "",
        
    )