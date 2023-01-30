import sys
import random
import pgf
from utils import (
    say,
    objects,
    items,
    item_modifiers,
    get_random_key,
    get_random_array_item,
    room_attributes,
    command_tree_examples,
    enemies,
)

absmodule = "RPGChatbot"
AVAILABLE_LANGS = ["Eng"]
grammar = pgf.readPGF("grammar/" + absmodule + ".pgf")
language = grammar.languages["RPGChatbotEng"]


class Player:
    """Represents the player object in the game."""

    def __init__(self) -> None:
        self.inventory = self.initialize_inventory()
        # Setting base stats.
        # TODO: Add randomisation and perhaps more attributes? E.g stamina, sneak, charm, magic
        self.power = 10
        self.health = 25

    def initialize_inventory(self) -> dict:
        inventory = {"Backpack": [], "Head": [], "Legs": []}
        return inventory

    def get_subinventory_items(self, subinventory) -> dict:
        """ Returns items from a specific subinventory. """
        pass

    def is_item_in_inventory(self, item) -> bool:
        """Checking if item is actually in inventory.
        Used for making sure that player cannot use items that they do not have.
        """
        pass

    def add_item_to_subinventory(self, item, subinventory) -> bool:
        """Adds an item to sub inventory if possible.
        Item name and subinventory is passed as arguments.
        """
        pass


class Item:
    """ Class that represents a single item. """

    def __init__(self, item_modifier=None, item_type=None) -> None:
        # Generating item
        self.name, self.base_name, self.modifier = self.generate_item(item_modifier, item_type)
        self.attributes = self.calculate_item_power()

    def generate_item(self, item_type, item_modifier) -> tuple:
        """ Generates an item either randomly or
         of a specific type determined by item_type argument"""
        base_name = item_type if item_type else get_random_key(items)
        if item_modifier and item_modifier in item_modifiers:
            modifier = item_modifier
        else:
            # Generating item modifier on a 40% chance.
            if (random.randint(0,100) < 40):
                # Generating random modifier
                modifier = get_random_key(item_modifiers)
                # To make legendary more rare, if it is rolled, another random chance has to be passed
                # or the modifier will be re-rolled.
                if modifier == "Legendary" and random.randint(0,10) < 5:
                    modifier = get_random_key(item_modifiers)
        # If in the end modifier exists, the item's name will be different.
        if modifier:
            # Constructing item name with modifier
            name = f"(ItemMod {modifier} {name})"
        else:
            name = base_name
        return name, base_name, modifier
    
    def calculate_item_power(self) -> int:
        """ Calculates the power of an item as integer. """
        base_attrs = items.get(self.base_name)
        modifier_formula = item_modifiers.get(self.modifier)
        # Items with 0 power cannot be enhanced with modifiers
        if base_attrs.power != 0:
            # Calling the modifier formula function and passing item base power to the function.
            power = modifier_formula(base_attrs.power)
        return power

        


        


class Enemy:
    def __init__(self) -> None:
        self.name = get_random_key(enemies)
        self.attributes = enemies.get(self.name)
        self.item = self.generate_primary_item()

    def generate_primary_item(self):
        """ Generates an item for an enemy that is equipped.
        """
        
        


class Object:
    def __init__(self, object_type=None) -> None:
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
        self.number = room_number
        # Generating entities eg. different entities for each way.
        self.paths = self.generate_entities()
        # Room attribute is an adjective that describes the room.
        # TODO: Making room attribute buff/nerf monsters/player.
        self.attribute = get_random_array_item(room_attributes)
        self.tell_room_intro()

    def print_room_intro(self) -> None:
        """Prints room entrance phrase in GF."""
        # Constructing the expression as string.
        expr_str = f"RoomIntro (RoomNumber {self.number}) {self.attribute}"
        # Reading the expression
        expr = pgf.readExpr(expr_str)
        # Linearizing the expression which turns the expression into text string.
        say(language.linearize(expr), "narrative")

    def generate_entities(self) -> dict:
        """Generates entities for a room. Entity can be an object or an enemy."""

        entities = {}
        # Possible directions in GF expressions format
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
                if random.randint(0, 100) > 40:
                    entities[name] = Enemy()
                else:
                    entities[name] = Object()
        return entities


class RPGBot:
    def __init__(self, args) -> None:
        """Initializes the chatbot."""

        # Initializing the GF and setting the language.

        # Initializing game objects
        self.player = Player()
        # Initializing room number as 1
        self.room_number = 1
        # And making the room with the number
        self.room = Room(self.room_number)
        # self.print_room_details(self.room)
        self.run_main_loop()
        pass

    def print_room_details(self, room) -> None:
        paths = room.paths
        ways = list(paths)
        for way in ways:
            entity = paths.get(way)
            print(type(entity))
            print(entity.name)
            print(entity.attributes)

    def run_main_loop(self):
        """Contains main input loop of the program."""
        prompt = pgf.readExpr("InputPrompt")
        # Running endless loop
        while True:
            say(language.linearize(prompt) + "?", "misc", start_lb=True)
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
                parseresult = language.parse(user_input, cat=pgf.readType(category))
            else:
                # Parsing command category by default
                parseresult = language.parse(user_input)
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
        say("Example inputs are shown below: ", "help", start_lb=True)
        say("-" * 20, "help")
        keys = list(command_tree_examples)
        for key in keys:
            say("[" + key + "]", "help")
            for expr_str in command_tree_examples.get(key):
                expr = pgf.readExpr(expr_str)
                say(language.linearize(expr), "help")
            print("\n")
        say("-" * 20, "help", end_lb=True)


def start_game(args):
    # Initializing library that allows for colored command-line printing.
    say("-" * 80, "program")
    say("Welcome to GF text-based roleplaying game!", "program")
    say(
        'Write "help" to see the list of the commands and "exit" to quit the program.',
        "program",
    )
    say("-" * 80, "program", end_lb=True)
    # Starting game.
    RPGBot(args)


if __name__ == "__main__":
    start_game(sys.argv)
