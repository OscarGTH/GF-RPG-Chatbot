
import random
from functools import reduce
from item import Item

class Player:
    """Represents the player object in the game."""

    def __init__(self) -> None:
        self.inventory = self.initialize_inventory()
        # Setting base stats.
        # TODO: Add randomisation and perhaps more attributes? E.g stamina, sneak, charm, magic
        self.power = random.randint(5, 15)
        self.health = random.randint(30, 50)
        self.in_combat = False
        self.combat_target = None
        # Adding starting weapon to player.
        self.add_item_to_subinventory(
            Item(item_type="Sword", item_modifier=None), "Backpack"
        )

    def start_combat(self, enemy_name):
        """ Starts combat with enemy. """
        self.in_combat = True
        self.combat_target = [enemy_name]

    def end_combat(self):
        """ Ends combat with enemy. """
        self.in_combat = False
        self.combat_target = None

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

    def get_weapon_sound(self, item_name) -> str:
        """ Returns weapon sound if it exists. """
        weapon = self.get_item_from_inventory(item_name)
        return weapon.sound

    def get_item_subinventory(self, item) -> str:
        """Returns the subinventory name where item is located in."""

        inventories = ["Head", "Legs", "Backpack"]
        for subinv in inventories:
            for sub_item in self.inventory.get(subinv):
                if sub_item.name == item:
                    return subinv

    def get_all_items_from_inventory(self) -> list:
        """ Returns all item references from all inventories. """
        inventories = self.inventory.keys()
        all_items = []
        for inv in inventories:
            all_items.extend(self.get_subinventory_items(inv))
        return all_items
 
    def get_item_from_inventory(self, item_name) -> object:
        """Returns an item reference from any inventory."""
        sub_inv = self.get_item_subinventory(item_name)
        if item := self.get_subinventory_item(item_name, sub_inv):
            return item
        else:
            return None

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
            return any(
                [
                    inv_item
                    for inv_item in self.inventory[subinventory]
                    if inv_item.name == item
                ]
            )

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
        self.refresh_player_stats(item=item, item_removed=True)
        return True

    def equip(self, item, from_loc, to_loc) -> bool:
        # Adding item to specific inventory slot.
        if self.add_item_to_subinventory(item, to_loc):
            # Removing previous item from previous sub inventory.
            self.remove_item_from_subinventory(item, from_loc)
            # Calculating stats again.
            self.refresh_player_stats()
            return True
        else:
            return False

    def is_item_equipped(self, item_name) -> bool:
        """Returns True if specific item is equipped in equipment slots."""

        sub_inv = self.get_item_subinventory(item_name)
        # If item was in some other subinventory than backpack, then it is equipped.
        if sub_inv and sub_inv != "Backpack":
            return True
        else:
            return False

    def remove_item_from_subinventory(self, item, subinventory) -> bool:
        """Removes an item from subinventory that matches the item object."""
        # Calling removal of the item.
        self.inventory[subinventory].remove(item)

    def refresh_player_stats(self, item=None, item_removed=False):
        """Refreshes player stats based on the equipped items."""
        total_power = self.power
        total_health = self.health

        # If item has been added, then bonus is calculated.
        if item_removed and item:
            # Removing item stats when item is unequipped.
            total_power = total_power - item.power
            total_health = total_health - item.health

        # Getting stats from items in subinventories except backpack.
        for subinv in ["Head", "Legs"]:
            if item := self.get_subinventory_items(subinv):
                total_power = total_power + item[0].power
                total_health = total_health + item[0].health

        # Updating calculated values to player stats.
        self.power = total_power
        self.health = total_health

    def check_for_respawn_item(self) -> bool:
        """ Checks if player is carrying item that can respawn them once. """
        if self.is_item_in_inventory("UndyingTotem", "Backpack"):
            return True
        else:
            return False

    def get_attack_power_with_weapon(self, item) -> int:
        """Calculates how much attack power player has with weapon and returns the value."""
        sub_inv = self.get_item_subinventory(item)
        weapon_obj = self.get_subinventory_item(item, sub_inv)
        return weapon_obj.power + self.power

    def reduce_player_health(self, reduction) -> None:
        """Reduces player health by a certain amount specified as argument."""

        self.health = self.health - reduction
