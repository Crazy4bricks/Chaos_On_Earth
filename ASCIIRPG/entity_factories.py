from components.ai import HostileEnemy
from components import consumable
from components.fighter import Fighter
from components.inventory import Inventory
from entity import Actor, Item
import color

player = Actor(
    char="@",
    color=color.white,
    name="Player",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=30, defense=2, power=5),
    inventory=Inventory(capacity=26),
    )

zombie = Actor(
    char="z",
    color=color.bright_green,
    name="Zombie",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=10, defense=0, power=3),
    inventory=Inventory(capacity=0),
    )
zombiehulk = Actor(
    char="Z",
    color=color.dark_green,
    name="Zombie Hulk",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=16, defense=1, power=4),
    inventory=Inventory(capacity=0),
    )
spatialcolor = Actor(
    char="O",
    color=color.chromatic[1],
    color_mode="chromatic",
    name="Spatial Ooze",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=10, defense=0, power=4),
    inventory=Inventory(capacity=0),
    )

confusion_scroll = Item(
    char="~",
    color=color.magenta,
    name="Confusion Scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)
fireball_scroll = Item(
    char="~",
    color=color.bright_red,
    name="Fireball Scroll",
    consumable=consumable.AreaDamageConsumable(damage=12, radius=3),
)
health_potion = Item(
    char="!",
    color=color.bright_red,
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=4),
)
lightning_scroll = Item(
    char="~",
    color=color.bright_blue,
    name="Lightning Scroll",
    consumable=consumable.SingleDamageConsumable(damage=20, maximum_range=5),
)