
import random
from utils import get_random_key
from constants import items, item_modifiers

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