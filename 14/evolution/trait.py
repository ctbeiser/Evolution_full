"""

"""
from enum import Enum
from functools import total_ordering

HARD_SHELL_THRESHOLD = 4


@total_ordering
class TraitSerialization:
    """
    This class is a mixin for Trait Enum, which allows it to serialize, deserialize, and appear in the GUI. This is
    necessary because Enums with a fixed set of members can't be extended.
    """
    def make_tree(self, tree, parent):
        """ Modify the ttk tree provided to add a representation of this data structure
        :param tree: a ttk Treeview widget object
        :param parent: the ttk reference to a row in the ttk Treeview under which this content should be added.
        """
        tree.insert(parent, 'end', text=("Trait: " + self.serialize()))

    def serialize(self):
        """ Returns a serialized representation of this data
        :return: String
        """
        return self.name.lower().replace("_", "-")

    @classmethod
    def deserialize(cls, data):
        """ Deserialize JSON-like data
        :param data: a String representing a trait
        :return: Trait
        """
        return cls(data)

    def __lt__(self, other):
        return self.serialize() < other.serialize()

    def __eq__(self, other):
        return self.serialize() == other.serialize()

traits = ["carnivore", "ambush", "burrowing", "climbing", "cooperation",
          "fat-tissue", "fertile", "foraging", "hard-shell", "herding",
          "horns", "long-neck", "pack-hunting", "scavenger", "symbiosis",
          "warning-call"]

trait_mapping = {trait.upper().replace("-", "_"): trait for trait in traits}

# Our Enum class, created using the functional Enum API, represents a Trait.
Trait = Enum(type=TraitSerialization, value="Trait", names=trait_mapping)
