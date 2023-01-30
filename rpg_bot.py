import sys
import random
import pgf
from utils import say, objects, items, get_random_key, command_tree_examples, enemies

absmodule = "RPGChatbot"
AVAILABLE_LANGS = ["Eng"]


class Player:
    """Represents the player object in the game."""

    def __init__(self) -> None:
        print("Player created.")


class Item:
    def __init__(self) -> None:
        print("Item created.")


class Enemy:
    def __init__(self) -> None:
        print("Enemy created")
        self.name = get_random_key(enemies)
        self.attributes = enemies.get(self.name)


class Object:
    def __init__(self, object_type=None) -> None:
        print("Object created")
        # Creating object of specific type.
        if object_type:
            self.name = object_type
        else:
            # Randomly generate an object
            self.name = get_random_key(objects)
        # Get attributes that are related to the object.
        self.attributes = objects.get(self.name)


class Room:
    """Represents room object that is inside map."""

    def __init__(self, room_number) -> None:

        print(f"Room {room_number} created.")
        self.number = room_number
        self.paths = self.generate_entities()

    def generate_entities(self) -> dict:
        """Generates entities for a room. Entity can be an object or an enemy."""

        entities = {}
        dir_names = ["Infront", "Behind", "LeftSide", "RightSide"]
        # Randomly selecting a direction of where the door is.
        # It has to be forced, so player cannot get stuck.
        door_dir = random.randint(0, 3)
        # Looping over path names.
        for name in dir_names:
            if dir_names[door_dir] == name:
                entities[name] = Object(object_type="Door")
            else:
                # If entity does not have to be a Door,
                # then it is either enemy or an object.
                if random.randint(0, 100) > 50:
                    entities[name] = Enemy()
                else:
                    entities[name] = Object()
        return entities


class RPGBot:
    def __init__(self, args) -> None:
        """Initializes the chatbot."""

        # Initializing the GF and setting the language.
        grammar = pgf.readPGF("grammar/" + absmodule + ".pgf")
        langcode = "RPGChatbotEng"
        if len(sys.argv) > 1:
            if sys.argv[1] in AVAILABLE_LANGS:
                langcode = absmodule + sys.argv[1]
            else:
                say("Supplied language not available.", "program")
        # Initializing game objects
        self.player = Player()
        # Initializing room number as 1
        self.room_number = 1
        # And making the room with the number
        self.room = Room(self.room_number)
        print(self.room)
        self.lang = grammar.languages[langcode]
        self.run_main_loop()
        pass

    def run_main_loop(self):
        """Contains main input loop of the program."""

        # Running endless loop
        while True:
            say("Player input:", "program")
            user_input = input("")

            if user_input == "exit":
                break
            elif user_input == "help":
                self.help()
            else:
                if command := self.parse_command(user_input):
                    self.process_command(command)
                else:
                    pass

    def process_command(self, command):
        """Processes the GF parse tree and acts accordingly."""
        base_fun, args = command.unpack()
        if base_fun == "Move":
            print("So you wanna move")
        elif base_fun == "Attack":
            print("Attacking..")
        elif base_fun == "Loot":
            print("Looting..")
        elif base_fun == "Put":
            print("Moving items.")
        elif base_fun == "QDirectionQuery":
            print("Don't you know where to go?")
        elif base_fun == "QItemQuery":
            print("You have so many items..")
        else:
            print("Unknown category..")

    def parse_command(self, user_input, category=None) -> pgf.Expr:
        """Parses the user command in GF format and returns the parse tree."""
        try:
            # Category can be used to parse input from different category, such as a question.
            if category:
                parseresult = self.lang.parse(user_input, cat=pgf.readType(category))
            else:
                # Parsing command category by default
                parseresult = self.lang.parse(user_input)
            prob, tree = parseresult.__next__()
            return tree
        # Catching parse errors
        except pgf.ParseError:
            # If category is set, then it is already second try, so we print out error message.
            if category:
                say("Unfortunately, I could not understand you.", "program")
                return None
            else:
                # Setting category to question to try if input can then be parsed.
                return self.parse_command(user_input, category="Question")

    def help(self):
        """Prints out the possible commands."""
        say("\nExample inputs are shown below: ", "program")
        say("-"*20, "program")
        keys = list(command_tree_examples)
        for key in keys:
            say("[" + key + "]", "program")
            for expr_str in command_tree_examples.get(key):
                expr = pgf.readExpr(expr_str)
                say(self.lang.linearize(expr), "program")
            print("\n")
        say("-"*20 + "\n", "program")


def start_game(args):
    # Initializing library that allows for colored command-line printing.

    say("\nWelcome to GF-RPG Text-based dungeon game!", "program")
    say(
        'Write "help" to see the list of the commands and "exit" to quit the program.\n',
        "program",
    )
    RPGBot(args)


if __name__ == "__main__":
    start_game(sys.argv)
