from components.ai import HostileEnemy
from components import consumable, equippable
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from core.entity import Actor, Item
from utils import color


player = Actor(
    char="@",
    color=color.white,
    name="Player",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=30, base_defense=2, base_power=5),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=200),
)

orc = Actor(
    char="o",
    color=color.bright_green,
    name="Orc",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=0, base_power=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
)
troll = Actor(
    char="T",
    color=color.dark_green,
    name="Troll",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=16, base_defense=1, base_power=4),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100),
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
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
)
health_potion = Item(
    char="!",
    color=color.magenta,
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=4),
)
lightning_scroll = Item(
    char="~",
    color=color.yellow,
    name="Lightning Scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)

dagger = Item(
    char="/",
    color=color.bright_cyan,
    name="Dagger",
    equippable=equippable.Dagger()
)
sword = Item(
    char="/",
    color=color.bright_cyan,
    name="Sword",
    equippable=equippable.Sword()
)

leather_armor = Item(
    char="[",
    color=color.brown,
    name="Leather Armor",
    equippable=equippable.LeatherArmor()
)

chain_mail = Item(
    char="[",
    color=color.bright_cyan,
    name="ChainMail",
    equippable=equippable.LeatherArmor()
)

# Materials