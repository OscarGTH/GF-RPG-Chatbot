import random
import sys
import os
import time
import pgf
# Used for playing sound effects.
from colorama import init as colorama_init
from colorama import Fore, Back, Style
from pygame import mixer

# Initializing sound mixer
mixer.init()
colorama_init()

# PGF initialization
absmodule = "RPGChatbot"
AVAILABLE_LANGS = ["Eng"]
grammar = pgf.readPGF(absmodule + ".pgf")
language = grammar.languages["RPGChatbotEng"]

# Text color styles
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

def play_sounds(sound_name) -> None:
    """ Plays a sounds effect. """
    path = f"sounds/{sound_name}"
    sound_path = os.path.join(os.getcwd(), path)
    if os.path.isfile(sound_path):
        mixer.music.load(sound_path)
        mixer.music.play()


def linearize_expr(expression) -> str:
    """Reads expression string and returns it as linearized string."""
    return language.linearize(pgf.readExpr(expression))


def parse_command(user_input, category=None) -> pgf.Expr:
    """Parses the user command in GF format and returns the parse tree."""
    try:
        # Category can be used to parse input from different category, such as a question.
        if category:
            parseresult = language.parse(user_input, cat=pgf.readType(category))
        else:
            # Parsing command category by default
            parseresult = language.parse(user_input)
        prob, tree = parseresult.__next__()
        return tree
    # Catching parse errors
    except pgf.ParseError as ex:
        # If category is set, then it is already second try, so we print out error message.
        if category:
            # TODO: Add gf error message instead.
            say("Unfortunately, I could not understand you.", "program")
            return None
        else:
            # Setting category to question to try if input can then be parsed.
            return parse_command(user_input, category="Question")


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
