import sys
import random
from functools import reduce
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
    int_to_digit,
    expr_to_str,
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
        self.power = random.randint(5, 15)
        self.health = 40
        # Adding starting weapon to player.
        self.add_item_to_subinventory(
            Item(item_type="Sword", item_modifier="Sharp"), "Backpack"
        )

    def initialize_inventory(self) -> dict:
        inventory = {"Backpack": [], "Head": [], "Legs": []}
        return inventory

    def get_subinventory_item(self, item, subinventory) -> object:
        """Returns specific item by name from a specific subinventory."""
        item_object = [
            inv_item
            for inv_item in self.inventory[subinventory]
            if inv_item.name == item
        ]
        return item_object[0]

    def get_subinventory_items(self, subinventory) -> list:
        """Returns all items from a specific subinventory."""
        items = [
            inv_item
            for inv_item in self.inventory[subinventory]
        ]
        return items

    def is_item_in_inventory(self, item) -> bool:
        """Checking if item is actually in inventory.
        Used for making sure that player cannot use items that they do not have.
        """
        # Merging all inventory lists into one list to make searching easier.
        # Items are placed to the list with their string names instead of objects.
        all_items = [
            item.name
            for item in reduce(
                lambda a, b: a + b, [arr for arr in self.inventory.values()]
            )
        ]
        if item in all_items:
            return True
        else:
            return False

    def add_item_to_subinventory(self, item, subinventory) -> bool:
        """Adds an item to sub inventory if possible.
        Item name and subinventory is passed as arguments.
        """
        if subinventory in item.fits_to:
            self.inventory[subinventory].append(item)
            return True
        else:
            # TODO: Say about item not fitting there.
            return False

    def get_attack_power_with_weapon(self, item) -> int:
        """Calculates how much attack power player has with item and returns the value."""
        weapon_obj = self.get_subinventory_item(item, "Backpack")
        return weapon_obj.power + self.power

    def reduce_player_health(self, reduction) -> None:
        """Reduces player health by a certain amount specified as argument."""
        self.health = self.health - reduction


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
        self.base_attrs = items.get(self.base_name)
        self.power, self.health = self.calculate_item_stats()
        self.fits_to = self.base_attrs.get("fits")
        self.type = self.base_attrs.get("type")

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

    def reduce_enemy_health(self, reduction) -> None:
        """Reduces enemy health when attacked."""
        self.health = self.health - reduction


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
        # Linearizing the expression which turns the expression into text string.
        say(language.linearize(pgf.readExpr(expr_str)), "narrative")

    def get_entity_at_direction(self, direction) -> object:
        """Returns the entity that is in the direction of the argument."""
        entity = self.paths.get(direction)
        # Enemies as objects need to be wrapped in enemyobject wrapper.
        if entity.__class__.__name__ == "Enemy":
            return f"(EnemyObject {entity.name})"
        else:
            return entity.name

    def get_enemy_by_name(self, name) -> object:
        """Returns entity reference by name."""
        entities = list(self.paths.values())
        enemies = [ent for ent in entities if ent.__class__.__name__ == "Enemy"]
        enemy = [enemy for enemy in enemies if enemy.name == name]
        return enemy[0]

    def get_direction_of_entity(self, name) -> str:
        """Returns the direction of where the entity is."""

        for direction in self.paths:
            if self.paths.get(direction).name == name:
                return direction

    def remove_entity_by_name(self, name) -> None:
        """Removes entity by name and replaces it with a door."""

        direction = self.get_direction_of_entity(name)
        self.paths[direction] = Object(object_type="Door")

    def check_if_entity_exists(self, entity_type, entity_name) -> bool:
        """Checks if any of the paths in the room have a specific entity."""
        entity_list = list(self.paths.values())
        # Filtering out all unnecessary classes
        ents = [ent for ent in entity_list if ent.__class__.__name__ == entity_type]
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
                existing_entities = [ent.name for ent in entities.values()]
                # If entity does not have to be a Door,
                # then it is either enemy or an object.
                if random.randint(0, 100) > 40:
                    # Generating unique enemy to the direction.
                    entities[name] = self.generate_unique_entity(
                        existing_entities, "Enemy"
                    )
                else:
                    entities[name] = self.generate_unique_entity(
                        existing_entities, "Object"
                    )
        return entities

    def generate_unique_entity(self, existing_ents, entity_type):
        """Generates unique entity that is not already in any of the directions."""

        # Making list of entities that exist already.
        # Looping until unique entity is generated.
        while True:
            if entity_type == "Enemy":
                # Making new entity randomly.
                new_ent = Enemy()
            else:
                new_ent = Object()
            # If name of the new entity is not in existing entities list, then we can add it.
            if new_ent.name not in existing_ents:
                # Return the entity object
                return new_ent
            else:
                # If duplicate entity was generated, then we pass to try the process again.
                pass


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
        #self.print_room_details(self.room)
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
            user_input = input("\n")

            if user_input == "exit":
                break
            elif user_input == "help":
                self.help()
            else:
                if command := self.parse_command(user_input):
                    self.process_command(command)
                else:
                    pass

    def process_command(self, command, blocked_commands=[]):
        """Processes the GF parse tree and acts accordingly."""
        base_fun, args = command.unpack()
        if base_fun not in blocked_commands:

            if base_fun == "Move":
                if base_fun not in blocked_commands:
                    self.move(args)
            elif base_fun == "Attack":
                if base_fun not in blocked_commands:
                    self.attack(args)
            elif base_fun == "Loot":
                if base_fun not in blocked_commands:
                    self.loot(args)
            elif base_fun == "Put":
                self.put(args)
            elif base_fun == "QDirectionQuery":
                self.direction_query(args)
            elif base_fun == "QItemQuery":
                self.item_query(args)
            else:
                print("Unknown category..")
        else:
            say(language.linearize(pgf.readExpr("InvalidAction")), "program")

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
                # TODO: Add gf error message instead.
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
        string_arg = str(args[0])
        # If enemy has modifier, then it needs to be wrapped in parenthesis.
        if "EnemyMod" in string_arg:
            parsed_name = f"({string_arg})"
        else:
            # If enemy has no modifier, then name is without parenthesis.
            parsed_name = f"{string_arg}"
        # If enemy with the name exists, then it can be attacked.
        if self.room.check_if_entity_exists("Enemy", parsed_name):
            self.run_battle(args[1], parsed_name)
        else:
            say("Enemy not found.", "narrative")

    def run_battle(self, weapon_arg, enemy_name) -> bool:
        """Handles the battle loop."""
        # Getting enemy object
        enemy = self.room.get_enemy_by_name(enemy_name)
        # Player gets to attack first. If attack fails, exit battle.
        if not self.do_player_attack(weapon_arg, enemy):
            return True
        # Main battle loop that begins after first attack.
        while enemy.health > 0:
            # Enemy attacks after player
            self.do_enemy_attack(enemy)

            # Checking player health after enemy attack.
            if self.player.health > 0:
                # Telling how much health the player has left.
                say(
                    language.linearize(
                        pgf.readExpr(f"PlayerHealth {int_to_digit(self.player.health)}")
                    ),
                    "narrative",
                )
                attack_not_done = True
                # Repeating the loop until player attacks again.
                while attack_not_done:
                    say(
                        language.linearize(pgf.readExpr("BattlePrompt")) + "?",
                        "misc", start_lb=True
                    )
                    # Receiving command from player.
                    battle_input = input("")
                    # Player can show available commands.
                    if battle_input == "help":
                        self.help()
                    elif battle_input == "exit":
                        sys.exit(1)
                    else:
                        command = self.parse_command(battle_input)
                        base_fun, args = command.unpack()
                        # Process "Attack" command here to prevent starting the battle again.
                        if base_fun == "Attack":
                            # Making sure player is attacking the same enemy.
                            if expr_to_str("EnemyMod", args[0]) == enemy_name:
                                # If attack succeeds, then attack is marked as done.
                                if self.do_player_attack(args[1], enemy):
                                    attack_not_done = False
                                else:
                                    # Going back to the beginning of the player battle input loop,
                                    # as the used weapon did not exist.
                                    pass
                            else:
                                # TODO: say that player is already in a battle with enemy
                                say(
                                    "You are already fighting another enemy.",
                                    "narrative",
                                )
                                pass
                        else:
                            # Processing other commands but blocking moving and looting while fighting.
                            self.process_command(
                                command, blocked_commands=["Move", "Loot"]
                            )
            else:
                say(language.linearize(pgf.readExpr("PlayerDeath")) + ".", "neg_result")
                # Ending program.
                sys.exit(1)
        say(language.linearize(pgf.readExpr(f"EnemyDeath {enemy.name}")) + ".", "pos_result")
        # Looting the enemy's items.
        self.loot_enemy(enemy)
        # Removing the enemy after it has died.
        self.room.remove_entity_by_name(enemy.name)
        return True

    def loot_enemy(self, enemy):
        """ Handles  the process of looting the enemy after it has died. """

        # Getting possible loot that the item left behind.
        loot = enemy.item
        if loot:
            # Adding item to player's backpack
            self.player.add_item_to_subinventory(loot, "Backpack")
            # Telling that an item was found.
            say(language.linearize(pgf.readExpr(f"LootSuccess {loot.name}")), "pos_result")

    def do_enemy_attack(self, enemy) -> None:
        """Performs attack towards player."""
        attack_power = enemy.power
        # Randomizing damage in a range.
        realized_power = random.randint(attack_power - 5, attack_power + 5)
        enemy_attack_expr = pgf.readExpr(
            f"EnemyAttack {enemy.name} {int_to_digit(realized_power)}"
        )
        # Linearizing the expression
        say(language.linearize(enemy_attack_expr), "enemy_hit", start_lb=True)
        # Reducing player health
        self.player.reduce_player_health(realized_power)

    def do_player_attack(self, weapon_arg, enemy) -> bool:
        """Performs one attack towards enemy.
        Returns True if attack succeeded (if item existed.)
        """

        weapon = expr_to_str("ItemMod", weapon_arg)
        # Checking that weapon is in player's inventory.
        if self.player.is_item_in_inventory(weapon):
            power = self.player.get_attack_power_with_weapon(weapon)
            # Real attack power is randomized in range of attack power +- 3.
            realized_power = random.randint(power - 3, power + 3)
            player_attack_expr = pgf.readExpr(
                f"AttackSuccess {enemy.name} {int_to_digit(realized_power)}"
            )
            say(language.linearize(player_attack_expr), "player_hit")
            enemy.reduce_enemy_health(realized_power)
            if enemy.health > 0:
                # Announcing enemy health after player attack.
                say(
                    language.linearize(
                        pgf.readExpr(
                            f"EnemyHealth {enemy.name} {int_to_digit(enemy.health)}"
                        )
                    ),
                    "narrative",
                )
            return True
        else:
            say(language.linearize(pgf.readExpr(f"ItemMissing {weapon}")), "neg_result")
            return False

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
                parsed_name = string_arg[len("EnemyObject ") :]
        else:
            ent_type = "Object"
            parsed_name = f"{str(args[0])}"

        if self.room.check_if_entity_exists(ent_type, parsed_name):
            say("You can loot that.", "narrative")
        else:
            say("Entity cannot be found.", "narrative")

    def put(self, args):
        """Command for player put action."""
        say("Putting.", "narrative")
        print(args[0], args[1])

    def direction_query(self, args):
        """Command for player asking about what is in each direction"""

        direction = str(args[0])
        entity = self.room.get_entity_at_direction(direction)
        say(
            language.linearize(pgf.readExpr(f"ADirectionQuery {direction} {entity}")),
            "narrative",
        )

    def item_query(self, args):
        """Command for querying about inventory items."""
        location = str(args[0])
        say(language.linearize(pgf.readExpr(f"AItemQuery {location}")) + ":", "pos_result")
        items = self.player.get_subinventory_items(location)
        # If items are in subinventory, then we print them in a loop.
        if items:
            for item in items:
                # Printing each item without capitalization, because items names should always be lowercase.
                say(language.linearize(pgf.readExpr(f"{item.name}")), "pos_result", capitalize=False)
        else:
            say("-", "pos_result")


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
