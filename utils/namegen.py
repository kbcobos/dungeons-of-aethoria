import random

_PREFIJOS = [
    "Khar", "Mal", "Dun", "Aer", "Vor", "Sel", "Zar", "Nar",
    "Bel", "Ghor", "Thel", "Urd", "Vex", "Mor", "Kar", "Eld",
    "Shan", "Drak", "Omen", "Ivar", "Azan", "Reth", "Solm",
]

_RAICES = [
    "athos", "endra", "oria", "imur", "azar", "othis", "endral",
    "uroch", "ithia", "amar", "ondur", "elvar", "akhor", "ishna",
    "aleth", "umbar", "areth", "olgur", "indar", "ozrath",
]

_SUFIJOS_DUNGEON = [
    "Depths", "Tomb", "Keep", "Ruins", "Caverns", "Crypt",
    "Vaults", "Halls", "Warrens", "Abyss", "Lair", "Sanctum",
    "Pit", "Fortress", "Labyrinth", "Chasm",
]

_ADJ_SALA = [
    "Forgotten", "Cursed", "Sunken", "Ancient", "Rotting",
    "Hollow", "Shattered", "Ashen", "Silent", "Bleeding",
    "Frozen", "Smoldering", "Crumbling", "Forsaken", "Drowned",
    "Haunted", "Festering", "Twilit", "Grim", "Wretched",
]

_SUST_SALA = {
    "combat":   ["Chamber", "Hall", "Arena", "Passage", "Gallery", "Antechamber"],
    "treasure": ["Vault", "Cache", "Alcove", "Hoard", "Reliquary", "Trove"],
    "rest":     ["Alcove", "Hollow", "Refuge", "Sanctuary", "Nook", "Recess"],
    "merchant": ["Bazaar", "Stall", "Market", "Corner", "Exchange", "Den"],
    "trap":     ["Corridor", "Passage", "Threshold", "Crossing", "Gate", "Entry"],
    "mystery":  ["Shrine", "Altar", "Sanctum", "Nexus", "Circle", "Ruin"],
    "boss":     ["Throne Room", "Inner Sanctum", "Final Chamber", "Lair",
                 "Heart", "Core", "Domain"],
}


def generate_dungeon_name() -> str:
    """
    Genera un nombre unico para toda la mazmorra.
    Ejemplo: "The Sunken Vaults of Kharoria"
    """
    prefix = random.choice(_PREFIJOS)
    root   = random.choice(_RAICES)
    suffix = random.choice(_SUFIJOS_DUNGEON)
    adj    = random.choice(_ADJ_SALA)
    return f"The {adj} {suffix} of {prefix}{root}"


def generate_floor_name(floor: int) -> str:
    """
    Genera un nombre para un piso especifico.
    Ejemplo: "The Ashen Halls — Floor 3"
    """
    adj    = random.choice(_ADJ_SALA)
    suffix = random.choice(_SUFIJOS_DUNGEON)
    return f"The {adj} {suffix}"


def generate_room_name(room_type: str) -> str:
    """
    Genera un nombre para una sala segun su tipo.
    Ejemplo: "The Rotting Chamber", "The Cursed Vault"
    """
    adj   = random.choice(_ADJ_SALA)
    nouns = _SUST_SALA.get(room_type, ["Chamber"])
    noun  = random.choice(nouns)
    return f"The {adj} {noun}"


def generate_enemy_title(enemy_name: str) -> str:
    """
    Agrega un titulo aleatorio a un enemigo para variedad.
    Ejemplo: "Goblin Scout, the Wretched"
    """
    titles = [
        "the Cursed", "the Ancient", "the Forgotten", "the Rotting",
        "the Hollow", "the Relentless", "the Damned", "the Forsaken",
        "the Wretched", "the Twisted", "the Undying", "the Hateful",
    ]
    return f"{enemy_name}, {random.choice(titles)}"
