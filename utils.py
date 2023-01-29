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
