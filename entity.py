
from utils import get_random_key
from constants import objects

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

