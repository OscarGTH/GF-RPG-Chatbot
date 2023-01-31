import random
import sys
from colorama import init as colorama_init
from colorama import Fore, Back, Style
import time

STYLES = {
    "narrative": {"fore": Fore.LIGHTGREEN_EX, "back": Back.BLACK, "delay": True},
    "pos_result": {"fore": Fore.CYAN, "back": "", "delay": True},
    "neg_result": {"fore": Fore.YELLOW, "back": "", "delay": True},
    "player_hit": {"fore": Fore.LIGHTMAGENTA_EX, "back": "", "delay": True},
    "enemy_hit": {"fore": Fore.RED, "back": "", "delay": True},
    "program": {"fore": Fore.LIGHTBLUE_EX, "back": "", "delay": False},
    "misc": {"fore": Fore.LIGHTYELLOW_EX, "back": "", "delay": True},
    "help": {"fore": Fore.YELLOW, "back": "", "delay": False},
}

colorama_init()


def say(text, style, start_lb=False, end_lb=True, capitalize=True):
    if style in STYLES:
        text_style = STYLES.get(style)
        if capitalize:
            # Capitalizing the sentence
            text = text.capitalize()
        # If linebreaks need to be printed, then it's printed before the actual phrase.
        if start_lb:
            text = "\n" + text
        if end_lb:
            text = text + "\n"
        print_phrase(text, text_style)
    else:
        print(f"{Fore.RED} Invalid text color style. {Style.RESET_ALL}")


def print_phrase(phrase, style):
    """Prints a phrase one key at a time with small delay."""

    if style.get("delay") is not False:
        for character in phrase:
            sys.stdout.write(
                f"{style.get('back')}{style.get('fore')}{character}{Style.RESET_ALL}"
            )
            sys.stdout.flush()
            if random.randint(0, 10) == 9:
                seconds = "0." + str(random.randrange(1, 2, 1))
            else:
                seconds = "0.0" + str(random.randrange(5, 30, 1))
            time.sleep(float(seconds))
    else:
        print(f"{style.get('back')}{style.get('fore')}{phrase}{Style.RESET_ALL}")


def get_random_key(dictionary) -> str:
    """Select random key from a passed dictionary."""
    keys = list(dictionary)
    rand_key = random.choice(keys)
    return rand_key


def get_random_array_item(array) -> str:
    """Select random item from array."""
    rand_item = array[random.randint(0, len(array) - 1)]
    return rand_item


def int_to_digit(number) -> str:
    """Turns integer into GF digit format."""
    num_str = str(number)[::-1]
    result = ""
    for index, digit in enumerate(num_str):
        if index == 0:
            result = f"IDig D_{digit}"
        else:
            result = f"IIDig D_{digit} ({result})"
    return f"({result})"


def expr_to_str(expr_type, expr) -> str:
    """Converts expression to string."""
    item_str = str(expr)
    # Parsing name for item.
    if expr_type in item_str:
        item = f"({item_str})"
    else:
        item = item_str
    return item


# GF categories
# Path directions are named differently than moving directions, so lookup table needs to exist.
move_directions = {
    "Left": "LeftSide",
    "Right": "RightSide",
    "Forward": "Infront",
    "Backward": "Behind",
}
enemies = {
    "Minotaur": {"health": 40, "power": 25},
    "Orc": {"health": 20, "power": 8},
    "Goblin": {"health": 10, "power": 5},
    "Dragon": {"health": 90, "power": 20},
    "Bandit": {"health": 28, "power": 8},
    "Mouse": {"health": 5, "power": 1},
    "Tiger": {"health": 35, "power": 15},
}
enemy_attributes = ["Weak", "Strong"]
room_attributes = ["Damp", "Bright", "Dark", "Creepy", "Scary", "Peaceful"]
enemy_modifiers = ["Angry", "Happy", "Furious", "Old"]
objects = {
    "Boulder": {"lootable": False, "passable": False, "locked": False},
    "Chest": {"lootable": True, "passable": True, "locked": True},
    "Bag": {"lootable": True, "passable": True, "locked": False},
    "Exit": {"lootable": False, "passable": True, "locked": False},
    "Gate": {"lootable": False, "passable": True, "locked": True},
    "Wall": {"lootable": False, "passable": False, "locked": False},
    "Door": {"lootable": False, "passable": True, "locked": False},
}
# Items have attack power and health attribute, that the wearer gets as a bonus.
items = {
    "Sword": {"power": 7, "health": 0, "type": "weapon", "fits": ["Backpack"]},
    "Axe": {"power": 13, "health": 0, "type": "weapon", "fits": ["Backpack"]},
    "Hammer": {"power": 10, "health": 0, "type": "weapon", "fits": ["Backpack"]},
    "WizardStaff": {"power": 20, "health": 0, "type": "weapon", "fits": ["Backpack"]},
    "Key": {"power": 1, "health": 0, "type": "misc", "fits": ["Backpack"]},
    "ScottishKilt": {
        "power": 5,
        "health": 25,
        "type": "equip",
        "fits": ["Backpack", "Legs"],
    },
    "LeatherSkirt": {
        "power": 2,
        "health": 15,
        "type": "equip",
        "fits": ["Backpack", "Legs"],
    },
    "VikingHelmet": {
        "power": 12,
        "health": 10,
        "type": "equip",
        "fits": ["Backpack", "Head"],
    },
    "BaseballCap": {
        "power": 6,
        "health": 8,
        "type": "equip",
        "fits": ["Backpack", "Head"],
    },
}
item_modifiers = {
    "Sharp": lambda power, health: (power + 5, health),
    "Dull": lambda power, health: (power - 8, health),
    "Broken": lambda power, health: (power - 15, health - 10),
    "Legendary": lambda power, health: (power * 4, health * 4),
    "Magical": lambda power, health: (power * 2, health * 2),
    "Shiny": lambda power, health: (power + 15, health + 15),
    "Fiery": lambda power, health: (power + 20, health + 5),
    "Mysterious": lambda power, health: (power * 3, health + 30),
    "Frozen": lambda power, health: (power + 25, health + 10),
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
