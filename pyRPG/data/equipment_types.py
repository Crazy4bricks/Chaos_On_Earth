from enum import auto, Enum

class EquipmentType(Enum):
    WEAPON = auto()
    ARMOR = auto()
    
class MaterialType(Enum):
    FABRIC = auto() #Woven material
    METALLIC = auto() #
    WOODEN = auto()
    METAMATERIAL = auto() #Strange material, locally made
    EXOTIC = auto() #Otherworldly material, origins from abroad
    
    