"""

"""
from enum import Enum

HARD_SHELL_THRESHOLD = 4


class TraitSerialization:
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

traits = ["carnivore", "ambush", "burrowing", "climbing", "cooperation",
          "fat-tissue", "fertile", "foraging", "hard-shell", "herding",
          "horns", "long-neck", "pack-hunting", "scavenger", "symbiosis",
          "warning-call"]

trait_mapping = {trait.upper().replace("-", "_"): trait for trait in traits}

Trait = Enum(type=TraitSerialization, value="Trait", names=trait_mapping)
