import random
from utils import get_random_key
from constants import enemies, enemy_modifiers, item_modifiers
from item import Item

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
        """Generates a trait randomly and returns it."""
        trait = {}
        # Selecting either weak or strong.
        trait["type"] = random.choice(["Weak", "Strong"])
        # Randomly selecting item modifier
        trait[
            "modifier"
        ] = f"(ItemType {random.choice([mod for mod in item_modifiers])})"
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
