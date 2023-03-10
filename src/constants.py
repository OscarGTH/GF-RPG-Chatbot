# GF categories
# Path directions are named differently than moving directions, so lookup table needs to exist.
move_directions = {
    "Left": "LeftSide",
    "Right": "RightSide",
    "Forward": "Infront",
    "Backward": "Behind",
}
# TODO: Balance enemies.
enemies = {
    "Troll": {"health": 18, "power": 25},
    "Ghoul": {"health": 30, "power": 8},
    "Goblin": {"health": 10, "power": 5},
    "Dragon": {"health": 60, "power": 20},
    "GiantRat": {"health": 20, "power": 8},
    "Demon": {"health": 80, "power": 60},
    "Skeleton": {"health": 15, "power": 15},
    "Wizard": {"health": 25, "power": 30},
}

enemy_attributes = ["Weak", "Strong"]
room_attributes = ["Damp", "Bright", "Dark", "Creepy", "Scary", "Peaceful"]
enemy_modifiers = {
    "Weak": {
        "modifier": lambda power, health: (round(power * 0.5), round(health * 0.5)),
        "appears_from_room": 1,
        "loot_categories": ["Common"],
    },
    "Young": {
        "modifier": lambda power, health: (round(power * 0.75), round(health * 0.75)),
        "appears_from_room": 5,
        "loot_categories": ["Common", "Rare"],
    },
    "Veteran": {
        "modifier": lambda power, health: (round(power * 1.5), round(health * 1.5)),
        "appears_from_room": 12,
        "loot_categories": ["Common", "Rare", "Epic"],
    },
    "Beefy": {
        "modifier": lambda power, health: (power + 20, health * 7),
        "appears_from_room": 15,
        "loot_categories": ["Rare", "Epic", "Unique"],
    },
    "Rabid": {
        "modifier": lambda power, health: (power * 2.5, round(health * 0.75)),
        "appears_from_room": 10,
        "loot_categories": ["Rare", "Epic"],
    },
    "Infernal": {
        "modifier": lambda power, health: (round(power * 3), health * 5),
        "appears_from_room": 20,
        "loot_categories": ["Unique"],
    },
}
objects = {
    "Boulder": {"lootable": False, "passable": False, "locked": False},
    # Lootable objects.
    "Chest": {
        "lootable": True,
        "passable": False,
        "locked": True,
        "rarities": ["Epic", "Unique"],
    },
    "Bag": {
        "lootable": True,
        "passable": False,
        "locked": False,
        "rarities": ["Common", "Rare", "Epic"],
    },
    "PileOfBones": {
        "lootable": True,
        "passable": False,
        "locked": False,
        "rarities": ["Common"],
    },
    "Exit": {"lootable": False, "passable": True, "locked": False},
    "Gate": {"lootable": False, "passable": True, "locked": True},
    "Wall": {"lootable": False, "passable": False, "locked": False},
    "Door": {"lootable": False, "passable": True, "locked": False},
}
# Items have attack power and health attribute, that the wearer gets as a bonus.
items = {
    "Sword": {
        "power": 7,
        "health": 0,
        "type": "weapon",
        "rarity": "Common",
        "fits": ["Backpack"],
        "sound": "sword_hit.wav",
    },
    "Axe": {
        "power": 13,
        "health": 0,
        "type": "weapon",
        "rarity": "Rare",
        "fits": ["Backpack"],
        "sound": "axe_hit.wav",
    },
    "Hammer": {
        "power": 10,
        "health": 0,
        "type": "weapon",
        "rarity": "Common",
        "fits": ["Backpack"],
        "sound": "hammer_hit.wav",
    },
    "WizardStaff": {
        "power": 20,
        "health": 0,
        "type": "weapon",
        "rarity": "Epic",
        "fits": ["Backpack"],
        "sound": "magic_hit.wav",
    },
    "Key": {
        "power": 1,
        "health": 0,
        "type": "misc",
        "rarity": "Rare",
        "fits": ["Backpack"],
    },
    "UndyingTotem": {
        "power": 1,
        "health": 0,
        "type": "misc",
        "rarity": "Unique",
        "fits": ["Backpack"],
    },
    "PlatiniumSkirt": {
        "power": 10,
        "health": 25,
        "type": "equip",
        "rarity": "Epic",
        "fits": ["Backpack", "Legs"],
    },
    "LeatherSkirt": {
        "power": 5,
        "health": 15,
        "type": "equip",
        "rarity": "Rare",
        "fits": ["Backpack", "Legs"],
    },
    "VikingHelmet": {
        "power": 12,
        "health": 20,
        "type": "equip",
        "rarity": "Unique",
        "fits": ["Backpack", "Head"],
    },
    "BaseballCap": {
        "power": 6,
        "health": 10,
        "type": "equip",
        "rarity": "Common",
        "fits": ["Backpack", "Head"],
    },
}
item_modifiers = {
    "Sharp": {
        "modifier": lambda power, health: (power + 5, health),
        "rarity": "Rare",
    },
    "Dull": {"modifier": lambda power, health: (power - 8, health), "rarity": "Common"},
    "Broken": {
        "modifier": lambda power, health: (power - 15, health - 10),
        "rarity": "Common",
    },
    "Legendary": {
        "modifier": lambda power, health: (power * 4, health * 4),
        "rarity": "Unique",
    },
    "Magical": {
        "modifier": lambda power, health: (power * 2, health * 2),
        "rarity": "Epic",
    },
    "Shiny": {
        "modifier": lambda power, health: (power + 10, health + 15),
        "rarity": "Common",
    },
    "Fiery": {
        "modifier": lambda power, health: (power + 35, health + 30),
        "rarity": "Rare",
    },
    "Mysterious": {
        "modifier": lambda power, health: (power * 3, health + 30),
        "rarity": "Unique",
    },
    "Frozen": {
        "modifier": lambda power, health: (power + 45, health + 30),
        "rarity": "Epic",
    },
}
locations = ["Backpack", "Head", "Legs"]
room_modifiers = ["Damp", "Bright", "Dark", "Creepy", "Scary", "Peaceful"]
# Used in help command by linearizing these to show what can be said.
command_tree_examples = {
    "Descriptive": [
        "DescribeEnemy Demon",
        "DescribeEnemy (EnemyMod Young Goblin)",
    ],
    "Drop": ["Drop (ItemMod Mysterious PlatiniumSkirt)", "Drop WizardStaff"],
    "Equip": ["Equip (ItemMod Mysterious PlatiniumSkirt)", "Equip PlatiniumSkirt"],
    "Unequip": ["Unequip LeatherSkirt"],
    "Attack": [
        "Attack Goblin Hammer",
        "Attack (EnemyMod Young Goblin) (ItemMod Mysterious Sword)",
        "Attack (EnemyMod Young Goblin) Hammer",
        "Attack Dragon (ItemMod Mysterious Axe)",
    ],
    "Loot": ["Loot Chest", "Loot PileOfBones"],
    "Move": ["Move Backward", "Move Forward", "Move Left", "Move Right"],
    "Item Query": ["QItemQuery Backpack", "QItemQuery Legs", "QItemQuery Head"],
    "Direction Query": ["QDirectionQuery Infront", "QDirectionQuery Behind"],
}
