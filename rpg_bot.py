import sys
import random
import pgf
from utils import (
    say,
    objects,
    items,
    item_modifiers,
    enemy_modifiers,
    get_random_key,
    get_random_array_item,
    room_attributes,
    command_tree_examples,
    enemies,
)

absmodule = "RPGChatbot"
AVAILABLE_LANGS = ["Eng"]
grammar = pgf.readPGF(absmodule + ".pgf")
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
        """Returns items from a specific subinventory."""
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
    """Class that represents a single item."""

    def __init__(
        self, item_type=None, item_modifier=None, allow_modifiers=True
    ) -> None:
        # Used to manually disable modifiers from certain items.
        self.allow_mods = allow_modifiers
        # Generating item
        self.name, self.base_name, self.modifier = self.generate_item(
            item_type, item_modifier
        )
        self.power, self.health = self.calculate_item_stats()
        self.fits_to = items.get(self.base_name).get("fits")

    def generate_item(self, item_type, item_modifier) -> tuple:
        """Generates an item either randomly or
        of a specific type determined by item_type argument."""

        modifier = None
        base_name = item_type if item_type else get_random_key(items)
        if item_modifier and item_modifier in item_modifiers:
            modifier = item_modifier
        elif self.allow_mods:
            # Generating item modifier on a 40% chance.
            if random.randint(0, 100) < 40:
                # Generating random modifier
                modifier = get_random_key(item_modifiers)
                # To make legendary more rare, if it is rolled, another random chance has to be passed
                # or the modifier will be re-rolled.
                if modifier == "Legendary" and random.randint(0, 10) < 5:
                    modifier = get_random_key(item_modifiers)
        # If in the end modifier exists, the item's name will be different.
        if modifier:
            # Constructing item name with modifier
            name = f"(ItemMod {modifier} {base_name})"
        else:
            name = base_name
        return name, base_name, modifier

    def calculate_item_stats(self) -> int:
        """Calculates the bonuses of an item."""

        # Getting basic attributes of the item
        base_attrs = items.get(self.base_name)
        # Assigning the power to a variable for later use
        power = base_attrs.get("power")
        health = base_attrs.get("health")
        # If modifier has been set, then the power needs to be processed by the modifier formula.
        if self.modifier:
            # Getting the lamba function that acts as modifier formula.
            modifier_formula = item_modifiers.get(self.modifier)
            # Calling the modifier formula function to modify health and power.
            power, health = modifier_formula(power, health)
            # Blocking negative hp, so entities cannot be killed by equipping an item.
            health = health if health >= 1 else 0
        return power, health


class Enemy:
    def __init__(self, allocate_item=False, force_modifier=False) -> None:
        self.name, self.base_name = self.generate_enemy_names(force_modifier)
        self.base_attrs = enemies.get(self.base_name)
        self.item = self.generate_primary_item(allocate_item)
        # Calculating power after assigning possible item.
        self.power, self.health = self.calculate_enemy_stats()

    def generate_primary_item(self, allocate_item):
        """Generates an item for an enemy that is equipped."""

        item = None
        # Generating item for the enemy by chance or by forcing it through argument.
        if random.randint(0, 100) > 65 or allocate_item:
            item = Item()
        return item

    def generate_enemy_names(self, force_modifier):
        """Generates enemy modifiers such as 'Angry Dragon'"""
        base_name = get_random_key(enemies)
        name = base_name
        # Generate enemy modifier on roughly 40% chance
        if random.randint(0, 100) > 40 or force_modifier:
            # Getting random modifier
            modifier = get_random_key(enemy_modifiers)
            # Constructing name as GF expression
            name = f"(EnemyMod {modifier} {base_name})"
        return name, base_name

    def calculate_enemy_stats(self) -> int:
        """Calculates enemy power and health based on the item that the enemy has."""
        power = self.base_attrs.get("power")
        health = self.base_attrs.get("health")
        if self.item:
            power = power + self.item.power
            health = health + self.item.health
        return power, health


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
    """Represents room object."""

    def __init__(self, room_number) -> None:
        self.number = room_number
        # Generating entities eg. different entities for each way.
        self.paths = self.generate_entities()
        # Room attribute is an adjective that describes the room.
        # TODO: Making room attribute buff/nerf monsters/player.
        self.attribute = get_random_array_item(room_attributes)
        self.tell_room_intro()

    def tell_room_intro(self) -> None:
        """Prints room entrance phrase in GF."""
        # Constructing the expression as string.
        expr_str = f"RoomIntro (RoomNumber {self.number}) {self.attribute}"
        # Reading the expression
        expr = pgf.readExpr(expr_str)
        # Linearizing the expression which turns the expression into text string.
        say(language.linearize(expr), "narrative")
    
    def get_entity_at_direction(self, direction) -> object:
        """ Returns the entity that is in the direction of the argument. """
        entity = self.paths.get(direction)
        if entity.__class__.__name__ == "Enemy":
            print("Enemy was there..")
            return entity
        else:
            return entity

    def check_if_entity_exists(self, entity_type, entity_name) -> bool:
        """Checks if any of the paths in the room have a specific entity."""
        print(f"Finding {entity_name}")
        entity_list = list(self.paths.values())
        # Filtering out all unnecessary classes
        ents = [
            ent for ent in entity_list if ent.__class__.__name__ == entity_type
        ]
        # Checking if any of the remaining entities have the same name as what is searched.
        return any(ent for ent in ents if ent.name == entity_name)

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
        self.print_room_details(self.room)
        self.run_main_loop()
        pass

    def print_room_details(self, room) -> None:
        paths = room.paths
        ways = list(paths)
        for way in ways:
            entity = paths.get(way)
            print(entity.name)

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
            self.move(args)
        elif base_fun == "Attack":
            self.attack(args)
        elif base_fun == "Loot":
            self.loot(args)
        elif base_fun == "Put":
            self.put(args)
        elif base_fun == "QDirectionQuery":
            self.direction_query(args)
        elif base_fun == "QItemQuery":
            self.item_query(args)
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

    def move(self, args):
        """Command for player movement."""

        direction = str(args[0])
        if direction == "Forward":
            say("Moving forward", "narrative")
        elif direction == "Left":
            say("Moving left", "narrative")
        elif direction == "Right":
            say("Moving right", "narrative")
        else:
            say("Moving backward.", "narrative")

    def attack(self, args):
        """Command for player attack action."""
        say("Attacking.", "narrative")
        parsed_name = f"({str(args[0])})"
        if self.room.check_if_entity_exists("Enemy", parsed_name):
            say("You found the enemy.", "narrative")
        else:
            say("Enemy not found.","narrative")


    def loot(self, args):
        """Command for player loot action."""

        say("Looting.", "narrative")
        string_arg = str(args[0])
        # If looting target is enemy, then it is wrapped in EnemyObject expression
        if "EnemyObject" in string_arg:
            # Entity type will be Enemy in this case.
            ent_type = "Enemy"
            # If enemy has modifier, then everything is wrapped in parenthesis.
            if "EnemyMod" in string_arg:
                # Extracting the enemy from inside the EnemyObject expression
                start = string_arg.index("(") + 1
                end = string_arg.rindex(")")
                parsed_name = f"({string_arg[start:end]})" 
            else:
                # Removing just the enemy object expression to get bare enemy type.
                parsed_name = string_arg[len("EnemyObject "):]
        else:
            ent_type = "Object"
            parsed_name = f"{str(args[0])}"

        if self.room.check_if_entity_exists(ent_type, parsed_name):
            say("You can loot that.", "narrative")
        else:
            say("Entity cannot be found.","narrative")

    def put(self, args):
        """Command for player put action."""
        say("Putting.", "narrative")
        print(args[0], args[1])

    def direction_query(self, args):
        """Command for player asking about what is in each direction"""
        
        direction = str(args[0])
        result = self.room.get_entity_at_direction(direction)
        print(result)

    def item_query(self, args):
        """Command for querying about inventory items."""
        say("Items list there you go.", "narrative")

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
