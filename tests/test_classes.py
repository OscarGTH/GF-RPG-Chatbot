"""
Unit tests for the RPG bot.
"""
import unittest
from unittest import mock
import io
import sys
from player import Player
from item import Item
from entity import Object
from enemy import Enemy
from room import Room
from constants import items, item_modifiers, objects


class TestPlayer(unittest.TestCase):
    """Tests that target the class Player"""

    def setUp(self) -> None:
        self.player = Player()

    def test_player_health_is_set(self):
        """Making sure player can be created and it has health as attribute."""
        self.assertIsNotNone(self.player.health)
        self.assertGreater(self.player.health, 1)

    def test_player_power_is_set(self):
        """Making sure player can be created and it has power."""
        self.assertIsNotNone(self.player.power)
        self.assertGreater(self.player.power, 1)

    def test_player_inventory_is_created(self):
        """Asserting that inventory has all keys and the value is correct type."""
        self.assertTrue(
            all(
                sub_inv in self.player.inventory
                for sub_inv in ("Backpack", "Head", "Legs")
            )
        )

        self.assertEqual(self.player.inventory.get("Backpack"), [])


class TestItem(unittest.TestCase):
    """Tests that target the class Item"""

    def setUp(self) -> None:
        self.item = Item()

    def test_item_is_created(self):
        """Testing default item generation."""
        self.assertIsNotNone(self.item.base_name)
        self.assertIsNotNone(self.item.name)

    def test_item_with_modifier_is_created(self):
        """Tests that items with specific modifier can be created."""

        mod_item = Item(item_modifier="Legendary")
        self.assertEqual(mod_item.modifier, "Legendary")
        self.assertIn("(ItemMod Legendary ", mod_item.name)
        self.assertIsNotNone(mod_item.base_name)

    def test_basic_item_power_is_set_correctly(self):
        """Tests that an item has correct power value."""

        mod_item = Item(item_type="Sword", allow_modifiers=False)
        self.assertEqual(mod_item.base_name, "Sword")
        self.assertEqual(mod_item.name, "Sword")
        self.assertIsNone(mod_item.modifier)
        # Testing that created item power matches with the base power of the item.
        self.assertEqual(mod_item.power, items.get("Sword").get("power"))

    def test_modified_item_stats_are_set_correctly(self):
        """Tests that an item has correct power and health values with a modifier."""

        mod_item = Item(item_type="Sword", item_modifier="Sharp")
        self.assertEqual(mod_item.name, "(ItemMod Sharp Sword)")
        lamb_func = item_modifiers.get("Sharp")
        self.assertEqual(
            (mod_item.power, mod_item.health),
            lamb_func(
                items.get("Sword").get("power"), items.get("Sword").get("health")
            ),
        )

    def test_item_gets_assigned_fit(self):
        """Test that items have an attribute that determines where it can be moved to."""

        self.assertIsNotNone(self.item.fits_to)
        self.assertIn("Backpack", self.item.fits_to)


class TestEnemy(unittest.TestCase):
    """Tests that target the class Enemy"""

    def setUp(self):
        self.enemy = Enemy()

    def test_enemy_has_attributes(self):
        """Tests that basic attributes of enemy are present."""

        self.assertIsNotNone(self.enemy.name)
        self.assertIsNotNone(self.enemy.base_attrs)

    def test_enemy_has_health_and_power(self):
        """Tests that attributes has all necessary fields."""

        self.assertIn("health", self.enemy.base_attrs)
        self.assertIn("power", self.enemy.base_attrs)
        self.assertGreaterEqual(self.enemy.base_attrs.get("health"), 1)
        self.assertGreaterEqual(self.enemy.base_attrs.get("power"), 1)

    def test_enemy_can_have_item(self):
        """Test that enemy has the possibility to use an item."""
        self.enemy.item = Item(item_type="Sword", item_modifier="Sharp")
        self.assertEqual(self.enemy.item.base_name, "Sword")

    def test_item_affects_enemy_stats(self):
        """Test that enemy statistics are affected by item."""
        test_enemy = Enemy(allocate_item=True)
        # Tuples should not be equal, because items affect stats and all items provide some stats.
        self.assertNotEqual(
            (test_enemy.base_attrs.get("health"), test_enemy.base_attrs.get("power")),
            (test_enemy.health, test_enemy.power),
        )


class TestObject(unittest.TestCase):
    """Tests that target the class Object"""

    def setUp(self):
        self.test_obj = Object()

    def test_object_has_attributes(self):
        """Tests that basic attributes are set for an object entity."""

        self.assertIsNotNone(self.test_obj.name)
        self.assertIsNotNone(self.test_obj.attributes)

    def test_specific_object_creation(self):
        """Tests that specific objects can be created."""
        test_obj = Object(object_type="Boulder")
        self.assertEqual(test_obj.name, "Boulder")

    def test_object_has_correct_attributes(self):
        """Tests that specific object has correct attributes assigned."""
        test_obj = Object(object_type="Boulder")
        self.assertEqual(
            test_obj.attributes.get("lootable"), objects.get("Boulder").get("lootable")
        )
        self.assertEqual(
            test_obj.attributes.get("passable"), objects.get("Boulder").get("passable")
        )
        self.assertEqual(
            test_obj.attributes.get("locked"), objects.get("Boulder").get("locked")
        )


class TestRoom(unittest.TestCase):
    """Tests that target the class Room"""

    def setUp(self):
        # Supressing print statements due to room intros.
        sys.stdout = io.StringIO()
        self.room = Room(1)
        # Removing supression.
        sys.stdout = sys.__stdout__

    def test_room_has_correct_attributes(self):
        """Test that room object contains necessary attributes after creation."""
        self.assertIsNotNone(self.room.number)
        self.assertIsNotNone(self.room.paths)
        self.assertIsNotNone(self.room.attribute)

    def test_room_has_number(self):
        """Test that room has room number assigned."""
        self.assertEqual(1, self.room.number)

    def test_room_has_all_paths(self):
        """Test that room has 4 ways in total, 1 for each direction."""
        self.assertTrue(
            all(
                path in self.room.paths
                for path in ("Infront", "Behind", "LeftSide", "RightSide")
            )
        )

    def test_room_always_has_door(self):
        """Test that room has at least one door always."""
        # Getting path entities to a list (as objects)
        path_entities = list(self.room.paths.values())
        # Getting entity names into a list
        entity_names = [e.name for e in path_entities]
        self.assertIn("Door", entity_names)


if __name__ == "__main__":
    unittest.main()
