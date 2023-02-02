import sys
import random
from utils import (
    say,
    int_to_digit,
    expr_to_str,
    print_cross,
    linearize_expr,
    parse_command,
    play_sounds
)
from constants import command_tree_examples, move_directions
from player import Player
from room import Room



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
        play_sounds("sword_hit.mp3")
        # Running endless loop
        while True:
            say(linearize_expr("InputPrompt") + "?", "misc", start_lb=True)
            user_input = input("\n")

            if user_input == "exit":
                break
            elif user_input == "help":
                self.help()
            else:
                if command := parse_command(user_input):
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
            elif base_fun == "Drop":
                self.drop(args)
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
            say(linearize_expr("InvalidAction"), "program")

    

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
                    linearize_expr(f"MoveSuccess {move_direction}"),
                    "pos_result",
                    end_lb=True,
                )
                self.change_room()
            # Doors, gates, and exits etc.
            if not lootable and passable:
                if locked:
                    say(linearize_expr(f"ObjectLocked {entity.name}"), "neg_result")
                else:
                    say(
                        linearize_expr(f"MoveSuccess {move_direction}"),
                        "pos_result",
                        end_lb=True,
                    )
                    self.change_room()
            # Boulders etc.
            if not passable:
                say(linearize_expr(f"MoveFail {entity.name}"), "neg_result")
        # Enemies
        else:
            say(linearize_expr(f"MoveFail (EnemyObject {entity.name})"), "neg_result")

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
                    linearize_expr(f"PlayerHealth {int_to_digit(self.player.health)}"
                    ),
                    "narrative",
                )
                attack_not_done = True
                # Repeating the loop until player attacks again.
                while attack_not_done:
                    say(
                        linearize_expr("BattlePrompt") + "?",
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
                        if command := parse_command(battle_input):
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
                                        linearize_expr(
                                            f"BattleInvalidTarget {enemy.name}"
                                        ),
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
                    linearize_expr(f"FightResult {enemy.name} Win") + ".",
                    "neg_result",
                    end_lb=True,
                )
                say(linearize_expr("PlayerDeath") + ".", "neg_result")
                # Ending program.
                sys.exit(1)
        say(linearize_expr(f"FightResult {enemy.name} Lose") + ".", "neg_result")
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
                linearize_expr(f"LootSuccess {loot.name}"),
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
            linearize_expr(f"EnemyAttack {enemy.name} {int_to_digit(realized_power)}"),
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
            rand_range = random.randint(power - 3, power + 3)
            # Value shouldn't be less than 0.
            realized_power = rand_range if rand_range >= 0 else 0
            say(
                linearize_expr(
                    f"AttackSuccess {enemy.name} {int_to_digit(realized_power)}"
                ),
                "player_hit",
            )
            enemy.reduce_enemy_health(realized_power)
            if enemy.health > 0:
                # Announcing enemy health after player attack.
                say(
                    linearize_expr(
                        f"EnemyHealth {enemy.name} {int_to_digit(enemy.health)}"
                    ),
                    "narrative",
                )
            return True
        else:
            say(
                linearize_expr(f"ItemMissing {weapon}"),
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
                    say(linearize_expr(msg), "pos_result")
                else:
                    # Printing error message about unsuccessful loot action.
                    say(linearize_expr(msg), "neg_result")
            else:
                say(linearize_expr(f"ObjectMissing {parsed_name}"), "neg_result")
        else:
            say(linearize_expr("LootEnemyFail"), "neg_result")

    def equip(self, args, unequip=False):
        """Command for player equip/unequip item action."""
        item = expr_to_str("ItemMod", args[0])
        if self.player.is_item_in_inventory(item):
            # Getting the subinventory where the item is located.
            from_location = self.player.get_item_subinventory(item)

            # If location of the item is in backpack and player wants to unequip it
            # Then error message is shown.
            if from_location == "Backpack" and unequip:
                say(linearize_expr(f"UnequipFail {item}"), "neg_result")
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
                    # Checking if item is equipped, or unequipped.
                    if not unequip:
                        success = self.player.equip(
                            item_obj, from_location, to_location
                        )
                    else:
                        success = self.player.unequip(
                            item_obj, from_location, to_location
                        )
                    if success:
                        say(
                            linearize_expr(f"ItemMoveSuccess {item} {to_location}"),
                            "pos_result",
                        )
                    else:
                        say(linearize_expr(f"ItemMoveFail {item}"), "neg_result")
                else:
                    # Item slot was taken by some other item.
                    say(
                        linearize_expr(
                            f"ItemSlotTaken {items_in_sub_inv[0].name} {to_location}"
                        ),
                        "neg_result",
                    )
            else:
                # Item could not be equipped to any slot.
                say(linearize_expr(f"EquipFail {item}"), "neg_result")
        else:
            say(
                linearize_expr(f"ItemMissing {item}"),
                "neg_result",
                capitalize=False,
            )

    def open(self, args):
        """Command for player open action."""

        item = expr_to_str("ItemMod", args[0])
        entity = str(args[1])
        if self.player.is_item_in_inventory(item):
            item = self.player.get_item_from_inventory(item)
            # Only allowing the opening to work with keys.
            if item.base_name == "Key":
                # Trying to open the entity.
                succeeded, msg = self.room.open_entity_by_name(entity)
                # If opening succeeded, go here.
                if succeeded:
                    # Removing key from inventory.
                    self.player.remove_item_from_subinventory(item, "Backpack")
                    say(linearize_expr(msg), "pos_result")
                else:
                    # Printing error phrase if opening failed.
                    say(linearize_expr(msg), "neg_result")
            else:
                # Telling that the item cannot be used for opening anything.
                say(linearize_expr(f"InvalidUnlockItem {item.name}"), "neg_result")
        else:
            say(
                linearize_expr(f"ItemMissing {item}"),
                "neg_result",
                capitalize=False,
            )

    def drop(self, args):
        """Command for dropping items from inventory."""

        item = expr_to_str("ItemMod", args[0])
        if self.player.is_item_in_inventory(item):
            # Checking if item to be dropped is equipped.
            if self.player.is_item_equipped(item):
                # Unequipping item from equipment slot so statistic change is calculated.
                self.player.unequip(item)
            # Removing item from backpack.
            self.player.remove_item_from_subinventory(self.player.get_item_from_inventory(item), "Backpack")
            say(linearize_expr(f"DropSuccess {item}"), "pos_result")
        else:
            say(
                linearize_expr(f"ItemMissing {item}"),
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
                    linearize_expr(f"EnemyEncountered {entity.name} {entity.item.name}"),
                    "narrative",
                )
                return
        else:
            ent_name = entity.name
        say(
            linearize_expr(f"ADirectionQuery {direction} {ent_name}"),
            "narrative",
        )
        return

    def item_query(self, args):
        """Command for querying about inventory items."""
        location = str(args[0])
        say(
            linearize_expr(f"AItemQuery {location}") + ":",
            "pos_result",
        )
        items = self.player.get_subinventory_items(location)
        # If items are in subinventory, then we print them in a loop.
        if items:
            for item in items:
                # Printing each item without capitalization, because items names should always be lowercase.
                say("- " + linearize_expr(f"{item.name}"), "pos_result", capitalize=False, no_delay=True)
        else:
            say("-", "pos_result")

    def entity_query(self):
        """Command for asking what entities are in the current room."""
        entities = self.room.get_all_entity_names()
        linearized_ents = []
        # Looping over entities
        for entity in entities:
            # Linearizing expressions to strings.
            linearized_ents.append(linearize_expr(entity))
        # Printing the entities in cross format.
        print_cross(*linearized_ents)

    def describe_enemy(self, args):
        """Command for asking the description about some enemy."""

        enemy_name = expr_to_str("EnemyMod", args[0])
        # If entity exists, we can describe it.
        if self.room.check_if_entity_exists("Enemy", enemy_name):
            enemy = self.room.get_entity_by_name("Enemy", enemy_name)
            if enemy.item:
                expression = f"EnemyDescWithItem {enemy_name} {enemy.trait['type']} {enemy.trait['modifier']} {enemy.item.name}"
            else:
                expression = f"EnemyDescWithoutItem {enemy_name} {enemy.trait['type']} {enemy.trait['modifier']}"
            say(linearize_expr(expression), "narrative")

    def help(self):
        """Prints out the possible commands."""
        say("Example inputs are shown below: ", "help", start_lb=True)
        say("-" * 20, "help")
        keys = list(command_tree_examples)
        for key in keys:
            say("[" + key + "]", "help")
            for expr_str in command_tree_examples.get(key):
                say(linearize_expr(expr_str), "help")
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
