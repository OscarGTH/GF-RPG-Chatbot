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
    move_directions,
    print_cross,
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
        items = [inv_item for inv_item in self.inventory[subinventory]]
        return items
    
    def get_item_subinventory(self, item) -> str:
        """ Returns the subinventory name where item is located in."""

        inventories = ["Head","Legs","Backpack"]
        for subinv in inventories:
            for sub_item in self.inventory.get(subinv):
                if sub_item.name == item:
                    return subinv
                

    def is_item_in_inventory(self, item, subinventory=None) -> bool:
        """Checking if item is actually in inventory.
        Used for making sure that player cannot use items that they do not have.
        """
        if not subinventory:
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
        else:
            # Check if item is in subinventory.
            return any([inv_item for inv_item in self.inventory[subinventory] if inv_item.name == item])

    def add_item_to_subinventory(self, item, subinventory) -> bool:
        """Adds an item to sub inventory if possible.
        Item name and subinventory is passed as arguments.
        """
        if subinventory in item.fits_to:
            self.inventory[subinventory].append(item)
            return True
        else:
            return False

    def unequip(self, item, from_loc, to_loc) -> bool:
        # Removing item
        self.remove_item_from_subinventory(item, from_loc)
        # Adding it to other inventory
        self.add_item_to_subinventory(item, to_loc)
        # Calculating stats again.
        self.refresh_player_stats(item=item, addition=False)
        return True

    def equip(self, item, from_loc, to_loc) -> bool:
        # Adding item
        if self.add_item_to_subinventory(item, to_loc):
            # Removing old item
            self.remove_item_from_subinventory(item, from_loc)
            # Calculating stats again.
            self.refresh_player_stats()
            return True
        else:
            return False

    def remove_item_from_subinventory(self, item, subinventory) -> bool:
        """ Removes an item from subinventory. """
        # Calling removal of the item.
        self.inventory[subinventory].remove(item)

    def refresh_player_stats(self, item=None, addition=True):
        """ Refreshes player stats based on the equipped items. """
        total_power = self.power
        total_health = self.health
        subinvs = ["Head","Legs"]
        # Getting stats from items in subinventories except backpack.
        for subinv in subinvs:
            # If item is equipped, then stats are increased.
            if addition:
                if item := self.get_subinventory_items(subinv):
                    total_power = total_power + item[0].power
                    total_health = total_health + item[0].health
            else:
                # Removing item stats if it is unequipped.
                total_power = total_power - item.power
                total_health = total_health - item.health

        # Preventing health or power from dropping to 0 or below after item unequip/equip action.
        if total_power < 1:
            total_power = 1
        if total_health < 1:
            total_health = 1

        # Updating calculated values to player stats.
        self.power = total_power
        self.health = total_health

    def move_item_in_inventory(self, item, from_location, to_location):
        """ Moves an item between inventories. """
        item = self.get_subinventory_item(item, from_location)
        # Adding item to subinventory first.
        if self.add_item_to_subinventory(item, to_location):
            # Removing item from origin inventory.
            self.remove_item_from_subinventory(item, from_location)
            return True
        else:
            return False

    def get_attack_power_with_weapon(self, item) -> int:
        """Calculates how much attack power player has with weapon and returns the value."""
    
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
            modifier_formula = item_modifiers.get(self.modifier).get("modifier")
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
        # Trait makes enemy either weak or strong against some item attribute.
        self.trait = self.generate_trait()
    
    def generate_trait(self) -> dict:
        """ Generates a trait randomly and returns it."""
        trait = {}
        # Selecting either weak or strong.
        trait["type"] = random.choice(["Weak","Strong"])
        # Randomly selecting item modifier
        trait["modifier"] = f"(ItemType {random.choice([mod for mod in item_modifiers])})"
        return trait


    def generate_primary_item(self, allocate_item):
        """Generates an item for an enemy that is equipped."""

        item = None
        # Generating item for the enemy by chance or by forcing it through argument.
        if random.randint(0, 100) > 10 or allocate_item:
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
        say(language.linearize(pgf.readExpr(expr_str)), "narrative", start_lb=True)

    def get_entity_at_direction(self, direction) -> object:
        """Returns the entity that is in the direction of the argument."""
        return self.paths.get(direction)

    def get_entity_by_name(self, entity_type, name) -> object:
        """Returns entity reference by name."""
        entities = list(self.paths.values())
        entity_types = [ent for ent in entities if ent.__class__.__name__ == entity_type]
        entity = [ent for ent in entity_types if ent.name == name]
        return entity[0]
    
    def get_all_entity_names(self) -> list:
        """ Returns all entity names in the room as strings in a list. 
            Order of entities is the following:
            (Infront, Right, Behind, Left)
        """
        entitity_objs = list(self.paths.values())
        entities = [ent.name for ent in entitity_objs]
        return entities


    def get_direction_of_entity(self, name) -> str:
        """Returns the direction of where the entity is."""

        for direction in self.paths:
            if self.paths.get(direction).name == name:
                return direction

    def remove_entity_by_name(self, name) -> None:
        """Removes entity by name and replaces it with a door."""

        direction = self.get_direction_of_entity(name)
        self.paths[direction] = Object(object_type="PileOfBones")

    def open_entity_by_name(self, name) -> tuple:
        """ Opens entity if it can be opened.
            Returns tuple that contains the information 
            about whether the unlock succeeded and a message to be said.
         """
        if self.check_if_entity_exists("Object", name):
            direction = self.get_direction_of_entity(name)
            entity = self.get_entity_by_name("Object", name)
            # If object is locked then it can be also opened.
            if entity.attributes.get("locked"):
                # Opening the lock.
                entity.attributes["locked"] = False
                # Replacing the entity at direction with the modified version.
                self.paths[direction] = entity
                return (True, f"ObjectUnlocked {name}")
            else:
                return (False, f"ObjectInvalidUnlock {name}")
        else:
            return (False, f"ObjectMissing {name}")
    
    def loot_entity_by_name(self, name) -> tuple:
        """ Loots entity if it is open. """
        direction = self.get_direction_of_entity(name)
        entity = self.get_entity_by_name("Object", name)
        if entity.attributes.get("lootable"):
            # If entity is locked, we return None and an error message. 
            if entity.attributes.get("locked"):
                return (None, f"ObjectLocked {name}")
            else:

                possible_raritites = entity.attributes.get("rarities")
                loot_randomizer = random.randint(0,100)
                # 40% chance to get item of specific rarity with common modifier
                if loot_randomizer < 40:
                    # Filtering out items that cannot be in the entity loot table.
                    filt_items = [item for item in items if items.get(item).get("rarity") in possible_raritites]
                    filt_modifiers = [mod for mod in item_modifiers if item_modifiers[mod].get("rarity") in ["Common"]]
                # 40% chance to get common item with specific rarity modifier
                elif loot_randomizer >= 40 and loot_randomizer < 80:
                    # Item will be common, but modifier will be from specific rarities list.
                    filt_items = [item for item in items if items.get(item).get("rarity") in ["Common"]]
                    filt_modifiers = [mod for mod in item_modifiers if item_modifiers[mod].get("rarity") in possible_raritites]
                # 20% chance to get item with specific rarity and specific rarity modifier (The best case scenario)
                else:
                    # Item will have specific rarity and the modifier will have specific rarity as well.
                    filt_items = [item for item in items if items.get(item).get("rarity") in possible_raritites]
                    filt_modifiers = [mod for mod in item_modifiers if item_modifiers[mod].get("rarity") in possible_raritites]

                base_item = get_random_array_item(filt_items)
                item_mod = get_random_array_item(filt_modifiers)
                item = Item(item_type=base_item, item_modifier=item_mod)
                # Replacing the looted object with wall.
                self.paths[direction] = Object(object_type="Wall")
                return (item, f"LootSuccess {item.name}")
        else:
            return (None, f"ObjectInvalidLoot {name}")
        

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
        dir_names = ["Infront", "RightSide", "Behind", "LeftSide"]
        # Randomly selecting a direction of where the door is.
        # It has to be forced, so player cannot get stuck.
        door_dir = random.randint(0, 3)
        # Looping over path names.
        for name in dir_names:
            if dir_names[door_dir] == name:
                entities[name] = Object(object_type="Door")
            else:
                # List of entities that exist in the room.
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
        # self.print_room_details(self.room)
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
                self.move(args)
            elif base_fun == "Attack":
                self.attack(args)
            elif base_fun == "Loot":
                self.loot(args)
            elif base_fun == "Equip":
                self.equip(args)
            elif base_fun == "Unequip":
                self.equip(args, unequip=True)
            elif base_fun == "Open":
                self.open(args)
            elif base_fun == "QDirectionQuery":
                self.direction_query(args)
            elif base_fun == "QItemQuery":
                self.item_query(args)
            elif base_fun == "QEntityQuery":
                self.entity_query()
            elif base_fun == "DescribeEnemy":
                self.describe_enemy(args)
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
        except pgf.ParseError as ex:
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

        move_direction = str(args[0])
        room_direction = move_directions.get(move_direction)
        entity = self.room.get_entity_at_direction(room_direction)
        if entity.__class__.__name__ == "Object":
            lootable = entity.attributes.get("lootable")
            passable = entity.attributes.get("passable")
            locked = entity.attributes.get("locked")
            # Chests
            if lootable and passable:
                say(
                    self.to_lin(f"MoveSuccess {move_direction}"),
                    "pos_result",
                    end_lb=True,
                )
                self.change_room()
            # Doors, gates, and exits etc.
            if not lootable and passable:
                if locked:
                    say(self.to_lin(f"ObjectLocked {entity.name}"), "neg_result")
                else:
                    say(
                        self.to_lin(f"MoveSuccess {move_direction}"),
                        "pos_result",
                        end_lb=True,
                    )
                    self.change_room()
            # Boulders etc.
            if not passable:
                say(self.to_lin(f"MoveFail {entity.name}"), "neg_result")
        # Enemies
        else:
            say(self.to_lin(f"MoveFail (EnemyObject {entity.name})"), "neg_result")

    def change_room(self):
        """Changes the room that the player is in."""
        self.room_number = self.room_number + 1
        self.room = Room(self.room_number)

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
        enemy = self.room.get_entity_by_name("Enemy", enemy_name)
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
                        "misc",
                        start_lb=True,
                    )
                    # Receiving command from player.
                    battle_input = input("\n")
                    # Player can show available commands.
                    if battle_input == "help":
                        self.help()
                    elif battle_input == "exit":
                        sys.exit(1)
                    else:
                        if command := self.parse_command(battle_input):
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
                                    say(
                                        self.to_lin(f"BattleInvalidTarget {enemy.name}"),
                                        "neg_result",
                                    )
                                    pass
                            elif base_fun == "AttackSameTarget":
                                # Attacking same enemy as before.
                                if self.do_player_attack(args[0], enemy):
                                    attack_not_done = False
                                else:
                                    pass
                            else:
                                # Processing other commands but blocking moving and looting while fighting.
                                self.process_command(
                                    command, blocked_commands=["Move", "Loot", "Open"]
                                )
            else:
                say(
                    self.to_lin(f"FightResult {enemy.name} Win") + ".",
                    "neg_result",
                    end_lb=True,
                )
                say(self.to_lin("PlayerDeath") + ".", "neg_result")
                # Ending program.
                sys.exit(1)
        say(self.to_lin(f"FightResult {enemy.name} Lose") + ".", "neg_result")
        # Looting the enemy's items.
        self.loot_enemy(enemy)
        # Removing the enemy after it has died.
        self.room.remove_entity_by_name(enemy.name)
        return True

    def loot_enemy(self, enemy):
        """Handles  the process of looting the enemy after it has died."""

        # Getting possible loot that the item left behind.
        loot = enemy.item
        if loot:
            # Adding item to player's backpack
            self.player.add_item_to_subinventory(loot, "Backpack")
            # Telling that an item was found.
            say(
                language.linearize(pgf.readExpr(f"LootSuccess {loot.name}")),
                "pos_result",
                start_lb=True,
            )

    def do_enemy_attack(self, enemy) -> None:
        """Performs attack towards player."""
        attack_power = enemy.power
        # Randomizing damage in a range.
        realized_power = random.randint(attack_power - 5, attack_power + 5)
        if realized_power < 0:
            realized_power = 0
        # Linearizing the expression
        say(
            self.to_lin(f"EnemyAttack {enemy.name} {int_to_digit(realized_power)}"),
            "enemy_hit",
            start_lb=True,
        )
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
            say(
                self.to_lin(
                    f"AttackSuccess {enemy.name} {int_to_digit(realized_power)}"
                ),
                "player_hit",
            )
            enemy.reduce_enemy_health(realized_power)
            if enemy.health > 0:
                # Announcing enemy health after player attack.
                say(
                    self.to_lin(
                        f"EnemyHealth {enemy.name} {int_to_digit(enemy.health)}"
                    ),
                    "narrative",
                )
            return True
        else:
            say(
                self.to_lin(f"ItemMissing {weapon}"),
                "neg_result",
                capitalize=False,
            )
            return False

    def loot(self, args):
        """Command for player loot action."""

        parsed_name = f"{str(args[0])}"
        if "EnemyObject" not in parsed_name:
            if self.room.check_if_entity_exists("Object", parsed_name):
                item, msg = self.room.loot_entity_by_name(parsed_name)
                if item:
                    # Adding loot to inventory
                    self.player.add_item_to_subinventory(item, "Backpack")
                    # Telling that item has been found.
                    say(self.to_lin(msg), "pos_result")
                else:
                    # Printing error message about unsuccessful loot action.
                    say(self.to_lin(msg), "neg_result") 
            else:
                say(self.to_lin(f"ObjectMissing {parsed_name}"), "neg_result")
        else:
            say(self.to_lin("LootEnemyFail"), "neg_result")

    def equip(self, args, unequip=False):
        """Command for player equip/unequip item action."""
        item = expr_to_str("ItemMod", args[0])
        if self.player.is_item_in_inventory(item):
            # Getting the subinventory where the item is located.
            from_location = self.player.get_item_subinventory(item)

            # If location of the item is in backpack and player wants to unequip it
            # Then error message is shown.
            if from_location == "Backpack" and unequip:
                say(self.to_lin(f"UnequipFail {item}"), "neg_result")
                return
            # Getting the item object
            item_obj = self.player.get_subinventory_item(item, from_location)

            # If item needs to be equipped, then it is not going to backpack.
            if not unequip:
                to_locations = [loc for loc in item_obj.fits_to if loc != "Backpack"]
            else:
                # If player wants to unequip item, then target is always backpack.
                to_locations = ["Backpack"]

            if to_locations:
                # Getting the first element of the location array.
                # There will only be one element left at this point.
                to_location = to_locations[0]
                # Getting items in subinventory
                items_in_sub_inv = self.player.get_subinventory_items(to_location)
                # Subinventory is empty, then equip action is allowed.
                if to_location == "Backpack" or not items_in_sub_inv:
                    if not unequip:
                        success = self.player.equip(item_obj, from_location, to_location)
                    else:
                        success = self.player.unequip(item_obj, from_location, to_location)
                    if success:
                        say(self.to_lin(f"ItemMoveSuccess {item} {to_location}"),"pos_result")
                    else:
                        say(self.to_lin(f"ItemMoveFail {item}"), "neg_result")
                else:
                    # Item slot was taken by some other item.
                    say(self.to_lin(f"ItemSlotTaken {items_in_sub_inv[0].name} {to_location}"),"neg_result")
            else:
                print("Test")
                # Item could not be equipped to any slot.
                say(self.to_lin(f"EquipFail {item}"),"neg_result")
        else:
            say(
                self.to_lin(f"ItemMissing {item}"),
                "neg_result",
                capitalize=False,
            )

    
    def open(self, args):
        """ Command for player open action. """
        item = expr_to_str("ItemMod", args[0])
        entity = str(args[1])
        if self.player.is_item_in_inventory(item):
            succeeded, msg = self.room.open_entity_by_name(entity)
            # If opening succeeded, go here.
            if succeeded:
                # Removing key from inventory.
                self.player.remove_item_from_subinventory(item, "Backpack")
                say(self.to_lin(msg), "pos_result")
            else:
                # Printing error phrase if opening failed.
                say(self.to_lin(msg),"neg_result")
        else:
            say(
                self.to_lin(f"ItemMissing {item}"),
                "neg_result",
                capitalize=False,
            )

    def direction_query(self, args):
        """Command for player asking about what is in each direction"""

        direction = str(args[0])
        entity = self.room.get_entity_at_direction(direction)
        if entity.__class__.__name__ == "Enemy":
            ent_name = f"(EnemyObject {entity.name})"
            # If enemy has item, then a different answer is given.
            if entity.item:
                say(
                    self.to_lin(f"EnemyEncountered {entity.name} {entity.item.name}"),
                    "narrative",
                )
                return
        else:
            ent_name = entity.name
        say(
            self.to_lin(f"ADirectionQuery {direction} {ent_name}"),
            "narrative",
        )
        return

    def item_query(self, args):
        """Command for querying about inventory items."""
        location = str(args[0])
        say(
            language.linearize(pgf.readExpr(f"AItemQuery {location}")) + ":",
            "pos_result",
        )
        items = self.player.get_subinventory_items(location)
        # If items are in subinventory, then we print them in a loop.
        if items:
            for item in items:
                # Printing each item without capitalization, because items names should always be lowercase.
                say("- " + self.to_lin(f"{item.name}"), "pos_result", capitalize=False)
        else:
            say("-", "pos_result")

    def entity_query(self):
        """ Command for asking what entities are in the current room. """
        entities = self.room.get_all_entity_names()
        linearized_ents = []
        # Looping over entities
        for entity in entities:
            # Linearizing expressions to strings.
            linearized_ents.append(self.to_lin(entity))
        # Printing the entities in cross format.
        print_cross(*linearized_ents)
    
    def describe_enemy(self, args):
        """ Command for asking the description about some enemy. """

        enemy_name = expr_to_str("EnemyMod", args[0])
        # If entity exists, we can describe it.
        if self.room.check_if_entity_exists("Enemy", enemy_name):
            enemy = self.room.get_entity_by_name("Enemy", enemy_name)
            if enemy.item:
                expression = f"EnemyDescWithItem {enemy_name} {enemy.trait['type']} {enemy.trait['modifier']} {enemy.item.name}"
            else:
                expression = f"EnemyDescWithoutItem {enemy_name} {enemy.trait['type']} {enemy.trait['modifier']}"
            say(self.to_lin(expression), "narrative")




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

    def to_lin(self, expression) -> str:
        """Reads expression string and returns it as linearized string."""
        return language.linearize(pgf.readExpr(expression))


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
