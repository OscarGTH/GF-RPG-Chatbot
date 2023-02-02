import random
import sys
import os
import time
import pgf

# For auto-completions of input
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.completion import Completer, Completion

# Used for playing sound effects.
# TODO: find a version that works with WSL too.
# import simpleaudio as sa
import wave
from colorama import init as colorama_init
from colorama import Fore, Back, Style


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
    """Plays a sounds effect."""
    path = f"sounds/{sound_name}"
    sound_path = os.path.join(os.getcwd(), path)
    # if "wav" in sound_name and os.path.isfile(sound_path):
    # wave_read = wave.open(sound_path, 'rb')
    # wave_obj = sa.WaveObject.from_wave_read(wave_read)
    # play_obj = wave_obj.play()


def linearize_expr(expression) -> str:
    """Reads expression string and returns it as linearized string."""
    return language.linearize(pgf.readExpr(expression))


def parse_command(user_input, completer, category=None) -> pgf.Expr:
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
        # If category is set, then it is already second try, so we try to predict the input.
        if category:
            # Setting context information
            prediction = completer.get_prediction(user_input, None)
            if prediction != user_input:
                # Removing possible double whitespaces.
                # prediction = " ".join(prediction.split())
                say(f'Did you mean to say "{prediction}"?', "program")
            else:
                say("Unfortunately, I could not understand you.", "program")
            return None
        else:
            # Setting category to question to try if input can then be parsed.
            return parse_command(user_input, completer, category="Question")


def remove_duplicate_substring(string):
    """Removes duplicate occurences of substring next to each other,
    such as 'attack >beefy< beefy skeleton'"""
    words = string.split()
    return ' '.join([words[i] for i in range(len(words)) if (i == 0) or words[i] != words[i - 1]])


class GFCompleter(Completer):
    """Context aware input completer"""

    def get_prediction(
        self,
        sugg_string,
        possible_command,
    ):
        """Tries to predict incomplete input string as accurately as possible.
        Takes context into account, so it does not predict scenarios that cannot happen.
        """
        # Getting suggestion based on the suggestion string.
        suggestions = language.complete(sugg_string)
        try:
            # Getting first suggestion
            sugg = suggestions.__next__()
            term = sugg[1]
            # Saving possible command so it can be used to make better predictions.
            if not possible_command and sugg[2] == "Command":
                possible_command = sugg[3]
            # Catching enemies, items and objects as those need to be filtered to match context.
            if sugg[2] == "Enemy":
                term = linearize_expr(get_random_array_item(self.enemy_suggestions))
            # Catching items to add context.
            elif sugg[2] == "Item":
                key = None
                filtered_items = self.items
                # Matching possible command, to prevent suggesting items that do not fit the usual use case.
                # e.g using key to attack is not useful even if it would be the first suggestion from GF.
                if possible_command in ["Equip", "Unequip"]:
                    key = "equip"
                elif possible_command == "Attack":
                    key = "weapon"
                elif possible_command == "Open":
                    key = "misc"

                # If key was set, then some filtering needs to be done.
                if key:
                    # Filtering items by their type.
                    filtered = [i for i in self.items if i.type == key]
                    if filtered:
                        filtered_items = filtered
                # Choosing random item among filtered items
                chosen_item = get_random_array_item(filtered_items)
                # Setting the name of the item as the term.
                term = linearize_expr(chosen_item.name)
            elif sugg[2] == "Object":
                chosen_object = get_random_array_item(self.objects)
                # Setting keys for specific actions
                if possible_command == "Loot":
                    key = "lootable"
                elif possible_command == "Open":
                    key = "locked"
                
                if key:
                    filtered = [x for x in self.objects if x.attributes.get(key)]
                    if filtered:
                        chosen_object = filtered[0]
                term = linearize_expr(chosen_object.name)
            elif sugg[2] == "MoveDirection":
                # Predicting only valid directions.
                chosen_direction = get_random_array_item(self.valid_directions)
                term = linearize_expr(chosen_direction)

            # Constructing the word and removing possible duplicate substrings.
            built_word = remove_duplicate_substring(f"{sugg_string} {term}")
            # Calling itself recursively with previous and new term added together.
            # Eventually function will terminate when StopIteration is thrown.
            return self.get_prediction(built_word, possible_command)

        except StopIteration:
            # Returning final constructed string.
            return sugg_string

    def set_info(self, player, room):
        """Updates fresh information about the context,
        so input suggestions can be more smart.
        """
        self.player = player
        self.room = room
        # All enemy objects for better predictions.
        self.enemies = self.room.get_all_entities_by_type("Enemy")
        # Enemy names only or the enemy that the player is fighting.
        self.enemy_suggestions = (
            self.player.combat_target
            if self.player.in_combat
            else [enemy.name for enemy in self.enemies]
        )
        # Item objects for further analyzing.
        self.items = [item for item in self.player.get_all_items_from_inventory()]
        # Item names only
        self.item_suggestions = [item.name for item in self.items]
        # Object objects (class)
        self.objects = self.room.get_all_entities_by_type("Object")
        # Object names only
        self.obj_suggestions = [obj.name for obj in self.objects]
        # Directions where the player can move successfully.
        # Used for predictions.
        self.valid_directions = self.room.get_possible_moving_directions()

    def get_completions(self, document, complete_event):

        comp = language.complete(document.text)
        try:
            all_suggs = [x for x in comp]
            if all_suggs:
                yielded = []
                for sugg in all_suggs:
                    if sugg[2] == "Enemy":
                        for enemy in self.enemy_suggestions:
                            if enemy not in yielded:
                                yielded.append(enemy)
                                linearized = linearize_expr(enemy)
                                yield Completion(linearized, start_position=0)
                    elif sugg[2] == "Item":
                        for item in self.item_suggestions:
                            if item not in yielded:
                                yielded.append(item)
                                linearized = linearize_expr(item)
                                yield Completion(linearized, start_position=0)
                    elif sugg[2] == "Object":
                        for obj in self.obj_suggestion:
                            if obj not in yielded:
                                yielded.append(obj)
                                linearized = linearize_expr(obj)
                                yield Completion(linearized, start_position=0)
                    elif sugg[2] in ["Location", "MoveDirection", "QuestionDirection"]:
                        if sugg[1] not in yielded:
                            yielded.append(sugg[1])
                            yield Completion(sugg[1], start_position=0)
                    elif sugg[3] in [
                        "QDirectionQuery",
                        "Move",
                        "QItemQuery",
                        "Equip",
                        "Drop",
                        "Unequip",
                        "QEntityQuery",
                        "DescribeEnemy",
                        "Loot",
                        "Open",
                        "Object",
                        "Attack",
                    ]:
                        if sugg[1] not in yielded:
                            yielded.append(sugg[1])
                            yield Completion(sugg[1], start_position=0)
                    elif sugg[3] == "AttackSameTarget" and self.player.in_combat:
                        if sugg[1] not in yielded:
                            yielded.append(sugg[1])
                            yield Completion(sugg[1], start_position=0)
        except:
            pass


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
    if array:
        return random.choice(array)
    else:
        return ""


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
