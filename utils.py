import random
from colorama import init as colorama_init
from colorama import Fore, Back, Style

STYLES = {
        "narrative":{"fore": Fore.LIGHTGREEN_EX,"back":Back.BLACK},
        "pos_result": {"fore": Fore.GREEN, "back":""},
        "neg_result": {"fore": Fore.YELLOW, "back":""},
        "player_hit": {"fore": Fore.LIGHTBLUE_EX, "back":""},
        "enemy_hit": {"fore": Fore.RED, "back": ""},
        "program": {"fore": Fore.LIGHTBLUE_EX, "back":""},
        "misc": {"fore": Fore.LIGHTYELLOW_EX, "back":""},
        "help": {"fore": Fore.YELLOW, "back": ""},
}

colorama_init()


def say(text, style, start_lb=False, end_lb=False):
    if style in STYLES:
        colors = STYLES.get(style)
        # Capitalizing the sentence
        text = text.capitalize()
        # Constructing the string with colors.
        phrase = f"{colors.get('back')}{colors.get('fore')}{text}{Style.RESET_ALL}"
        # If linebreaks need to be printed, then it's printed before the actual phrase.
        if start_lb:
            print("\n")
        print(phrase)
        if end_lb:
            print("\n")
    else:
        print(f"{Fore.RED} Invalid text color style. {Style.RESET_ALL}")


def get_random_key(dictionary) -> str:
    """Select random key from a passed dictionary."""
    keys = list(dictionary)
    rand_key = random.choice(keys)
    return rand_key

def get_random_array_item(array) -> str:
    """ Select random item from array. """
    rand_item = array[random.randint(0, len(array) - 1)]
    return rand_item

# GF categories
enemies = {
    "Minotaur": {"health": 20, "power": 30},
    "Orc": {"health": 15, "power": 8},
    "Goblin": {"health": 5, "power": 5},
    "Dragon": {"health": 60, "power": 25},
    "Bandit": {"health": 12, "power": 15},
    "Mouse": {"health": 3, "power": 1},
    "Tiger": {"health": 10, "power": 20},
}
enemy_attributes = ["Weak", "Strong"]
room_attributes = ["Damp", "Bright", "Dark", "Creepy", "Scary", "Peaceful"]
enemy_modifiers = ["Angry", "Happy", "Furious", "Old"]
objects = {
    "Boulder": {"lootable": False, "passable": False, "locked": False},
    "Chest": {"lootable": True, "passable": True, "locked": True},
    "Bag": {"lootable": True, "passable": True, "locked": False},
    "Exit": {"lootable": False, "passable": True, "locked": False},
    "Gate": {"lootable": False, "passable": False, "locked": True},
    "Wall": {"lootable": False, "passable": False, "locked": False},
    "Door": {"lootable": False, "passable": True, "locked": False},
}
# Items have attack power and health attribute, that the wearer gets as a bonus.
items = {
    "Sword": {"power": 13, "health": 0, "fits": ["Backpack"]},
    "Axe": {"power": 18, "health": 0, "fits": ["Backpack"]},
    "Hammer": {"power": 15, "health": 0, "fits": ["Backpack"]},
    "WizardStaff": {"power": 20, "health": 0, "fits": ["Backpack"]},
    "Key": {"power": 1, "health": 0, "fits": ["Backpack"]},
    "ScottishKilt": {"power": 5, "health": 25,  "fits": ["Backpack", "Legs"]},
    "LeatherSkirt": {"power": 2, "health": 15, "fits": ["Backpack", "Legs"]},
    "VikingHelmet": {"power": 12, "health": 10, "fits": ["Backpack", "Head"]},
    "BaseballCap": {"power": 6,  "health": 8, "fits": ["Backpack", "Head"]},
}
item_modifiers = {
    "Sharp": lambda power, health : (10 + power, health),
    "Dull": lambda power, health : (power - 8, health) ,
    "Broken": lambda power, health : (power - 15, health - 10),
    "Legendary": lambda power, health : (power * 4, health * 4),
    "Magical": lambda power, health : (power * 2, health * 2),
    "Shiny": lambda power, health : (power + 15 , health + 15),
    "Fiery": lambda power, health : (power + 20, health + 5),
    "Mysterious": lambda power, health : (power * 3, health + 30),
    "Frozen": lambda power, health : (power + 25, health + 10),
}
locations = ["Backpack", "Head", "Legs"]
room_modifiers = ["Damp", "Bright", "Dark", "Creepy", "Scary", "Peaceful"]
# Used in help command by linearizing these to show what can be said.
command_tree_examples = {
    "Descriptive": ["DescribeEnemy Mouse", "DescribeEnemy (EnemyMod Old Goblin)"],
    "Drop": ["Drop (ItemMod Mysterious ScottishKilt)", "Drop WizardStaff"],
    "Put": ["Put (ItemMod Mysterious ScottishKilt) Legs", "Put ScottishKilt Legs"],
    "Attack": [
        "Attack Minotaur Hammer",
        "Attack (EnemyMod Happy Orc) (ItemMod Mysterious Sword)",
        "Attack (EnemyMod Happy Orc) Hammer",
        "Attack Orc (ItemMod Mysterious Axe)",
    ],
    "Loot": ["Loot Chest"],
    "Move": ["Move Backward", "Move Forward", "Move Left", "Move Right"],
    "Item Query": ["QItemQuery Backpack", "QItemQuery Legs", "QItemQuery Head"],
    "Direction Query": ["QDirectionQuery Infront"],
}
