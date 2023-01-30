from colorama import init as colorama_init
from colorama import Fore, Back, Style

STYLES = {
    "narrative": Fore.LIGHTBLUE_EX,
    "pos_result": Fore.GREEN,
    "neg_result": Fore.YELLOW,
    "player_hit": Fore.LIGHTBLUE_EX,
    "enemy_hit": Fore.RED,
    "program": Fore.LIGHTRED_EX,
}

colorama_init()


def say(text, style):
    if style in STYLES:
        print(f"{STYLES.get(style)}{text}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED} Invalid text color style. {Style.RESET_ALL}")
# GF categories
enemies = ["Minotaur", "Orc", "Goblin", "Dragon", "Bandit", "Mouse", "Tiger"]
enemy_attributes = ["Weak","Strong"]
enemy_modifiers = ["Angry","Happy","Furious","Old"]
objects = ["Boulder","Chest","Bag", "Exit", "Gate", "Wall"]
items = ["Sword","Axe","Hammer","WizardStaff","Key","ScottishKilt","LeatherSkirt","VikingHelmet","BaseballCap"]
item_modifiers = ["Sharp","Dull","Broken","Legendary","Magical","Shiny","Fiery","Mysterious","Frozen"]
locations = ["Backpack","Head","Legs"]
room_modifiers = ["Damp", "Bright", "Dark", "Creepy", "Scary", "Peaceful"]

