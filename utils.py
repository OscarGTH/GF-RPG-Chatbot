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


def say(
    text,
    style,
    start_lb=False,
    end_lb=True,
    capitalize=True,
    no_delay=False,
    line_end="\n",
):
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
        print_phrase(text, text_style, line_end, no_delay)
    else:
        print(f"{Fore.RED} Invalid text color style. {Style.RESET_ALL}")


def print_cross(up, right, down, left):
    """Prints a visualisation of 4 strings in a cross format."""
    separator = "- - - - + - - - -"
    mid_middle_point = (left + separator).index("+")
    # Calculating middle points of the strings
    up_middle_point = round(len(up) / 2 + 1) if len(up) % 2 else round(len(up) / 2)
    down_middle_point = (
        round(len(down) / 2 + 1) if len(down) % 2 else round(len(down) / 2)
    )
    # Printing out the cross formation
    say((" " * (mid_middle_point - up_middle_point)) + up, "pos_result")
    say((" " * (mid_middle_point)) + "|", "pos_result", no_delay=True, line_end="")
    say(left + separator + right, "pos_result", capitalize=False)
    say((" " * (mid_middle_point)) + "|", "pos_result", no_delay=True, line_end="")
    say((" " * (mid_middle_point - down_middle_point)) + down, "pos_result")


def print_phrase(phrase, style, line_end, no_delay):
    """Prints a phrase one key at a time with small delay."""

    if style.get("delay") is not False and no_delay is False:
        for character in phrase:
            sys.stdout.write(
                f"{style.get('back')}{style.get('fore')}{character}{Style.RESET_ALL}"
            )
            sys.stdout.flush()
            # Making a longer pause on a 1/15 chance.
            if random.randint(0, 15) == 1:
                seconds = "0." + str(random.randrange(1, 2, 1))
            else:
                seconds = "0.0" + str(random.randrange(1, 15, 1))
            time.sleep(float(seconds))
    else:
        print(
            f"{style.get('back')}{style.get('fore')}{phrase}{Style.RESET_ALL}",
            end=line_end,
        )


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
# TODO: Balance enemies.
enemies = {
    "Troll": {"health": 30, "power": 25},
    "Ghoul": {"health": 20, "power": 8},
    "Goblin": {"health": 10, "power": 5},
    "Dragon": {"health": 90, "power": 20},
    "GiantRat": {"health": 28, "power": 8},
    "Demon": {"health": 80, "power": 60},
    "Skeleton": {"health": 35, "power": 15},
    "Wizard": {"health": 40, "power": 35},
}

enemy_attributes = ["Weak", "Strong"]
room_attributes = ["Damp", "Bright", "Dark", "Creepy", "Scary", "Peaceful"]
enemy_modifiers = ["Infernal", "Veteran", "Young", "Teenager", "Weak"]
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
    },
    "Axe": {
        "power": 13,
        "health": 0,
        "type": "weapon",
        "rarity": "Rare",
        "fits": ["Backpack"],
    },
    "Hammer": {
        "power": 10,
        "health": 0,
        "type": "weapon",
        "rarity": "Common",
        "fits": ["Backpack"],
    },
    "WizardStaff": {
        "power": 20,
        "health": 0,
        "type": "weapon",
        "rarity": "Epic",
        "fits": ["Backpack"],
    },
    "Key": {
        "power": 1,
        "health": 0,
        "type": "misc",
        "rarity": "Rare",
        "fits": ["Backpack"],
    },
    "PlatiniumSkirt": {
        "power": 5,
        "health": 25,
        "type": "equip",
        "rarity": "Epic",
        "fits": ["Backpack", "Legs"],
    },
    "LeatherSkirt": {
        "power": 2,
        "health": 15,
        "type": "equip",
        "rarity": "Rare",
        "fits": ["Backpack", "Legs"],
    },
    "VikingHelmet": {
        "power": 12,
        "health": 10,
        "type": "equip",
        "rarity": "Unique",
        "fits": ["Backpack", "Head"],
    },
    "BaseballCap": {
        "power": 6,
        "health": 8,
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
        "modifier": lambda power, health: (power + 16, health + 5),
        "rarity": "Rare",
    },
    "Mysterious": {
        "modifier": lambda power, health: (power * 3, health + 30),
        "rarity": "Unique",
    },
    "Frozen": {
        "modifier": lambda power, health: (power + 18, health + 10),
        "rarity": "Epic",
    },
}
locations = ["Backpack", "Head", "Legs"]
room_modifiers = ["Damp", "Bright", "Dark", "Creepy", "Scary", "Peaceful"]
# Used in help command by linearizing these to show what can be said.
command_tree_examples = {
    "Descriptive": ["DescribeEnemy Demon", "DescribeEnemy (EnemyMod Young Goblin)"],
    "Drop": ["Drop (ItemMod Mysterious PlatiniumSkirt)", "Drop WizardStaff"],
    "Put": ["Put (ItemMod Mysterious PlatiniumSkirt) Legs", "Put PlatiniumSkirt Legs"],
    "Attack": [
        "Attack Goblin Hammer",
        "Attack (EnemyMod Young Goblin) (ItemMod Mysterious Sword)",
        "Attack (EnemyMod Young Goblin) Hammer",
        "Attack Dragon (ItemMod Mysterious Axe)",
    ],
    "Loot": ["Loot Chest"],
    "Move": ["Move Backward", "Move Forward", "Move Left", "Move Right"],
    "Item Query": ["QItemQuery Backpack", "QItemQuery Legs", "QItemQuery Head"],
    "Direction Query": ["QDirectionQuery Infront"],
}
