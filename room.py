import random
from utils import get_random_array_item, say, linearize_expr
from constants import room_attributes, items, item_modifiers, move_directions
from entity import Object
from enemy import Enemy
from item import Item


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
        say(linearize_expr(expr_str), "narrative", start_lb=True)

    def get_entity_at_direction(self, direction) -> object:
        """Returns the entity that is in the direction of the argument."""
        return self.paths.get(direction)

    def get_entity_by_name(self, entity_type, name) -> object:
        """Returns entity reference by name."""
        entities = list(self.paths.values())
        entity_types = [
            ent for ent in entities if ent.__class__.__name__ == entity_type
        ]
        entity = [ent for ent in entity_types if ent.name == name]
        return entity[0]

    def get_all_entity_names(self) -> list:
        """Returns all entity names in the room as strings in a list.
        Order of entities is the following:
        (Infront, Right, Behind, Left)
        """
        entitity_objs = list(self.paths.values())
        entities = [ent.name for ent in entitity_objs]
        return entities

    def get_possible_moving_directions(self) -> list:
        """Returns list of directions where the player can move."""
        entities = self.get_all_entities_by_type("Object")
        directions = []
        for ent in entities:
            # Get passable objects and return move directions instead of entity directions.
            passable = [
                key
                for key, val in move_directions.items()
                if val == self.get_direction_of_entity(ent.name)
                and ent.attributes.get("passable")
            ]
            if passable:
                directions.append(passable[0])
        return directions

    def get_all_entities_by_type(self, entity_type) -> list:
        """Returns all entity names"""
        entity_objs = list(self.paths.values())
        entity_types = [
            ent for ent in entity_objs if ent.__class__.__name__ == entity_type
        ]
        return entity_types

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
        """Opens entity if it can be opened.
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
        """Loots entity if it is open."""
        direction = self.get_direction_of_entity(name)
        entity = self.get_entity_by_name("Object", name)
        if entity.attributes.get("lootable"):
            # If entity is locked, we return None and an error message.
            if entity.attributes.get("locked"):
                return (None, f"ObjectLocked {name}")
            else:

                possible_raritites = entity.attributes.get("rarities")
                loot_randomizer = random.randint(0, 100)
                # 40% chance to get item of specific rarity with common modifier
                if loot_randomizer < 40:
                    # Filtering out items that cannot be in the entity loot table.
                    filt_items = [
                        item
                        for item in items
                        if items.get(item).get("rarity") in possible_raritites
                    ]
                    filt_modifiers = [
                        mod
                        for mod in item_modifiers
                        if item_modifiers[mod].get("rarity") in ["Common"]
                    ]
                # 40% chance to get common item with specific rarity modifier
                elif loot_randomizer >= 40 and loot_randomizer < 80:
                    # Item will be common, but modifier will be from specific rarities list.
                    filt_items = [
                        item
                        for item in items
                        if items.get(item).get("rarity") in ["Common"]
                    ]
                    filt_modifiers = [
                        mod
                        for mod in item_modifiers
                        if item_modifiers[mod].get("rarity") in possible_raritites
                    ]
                # 20% chance to get item with specific rarity and specific rarity modifier (The best case scenario)
                else:
                    # Item will have specific rarity and the modifier will have specific rarity as well.
                    filt_items = [
                        item
                        for item in items
                        if items.get(item).get("rarity") in possible_raritites
                    ]
                    filt_modifiers = [
                        mod
                        for mod in item_modifiers
                        if item_modifiers[mod].get("rarity") in possible_raritites
                    ]

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
