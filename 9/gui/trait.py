"""

"""
from enum import Enum

HARD_SHELL_THRESHOLD = 4


class TraitSerialization:
    def make_tree(self, tree, parent):
        tree.insert(parent, 'end', text=("Trait: " + self.serialize()))

    def serialize(self):
        return self.name.lower().replace("_", "-")

    @classmethod
    def deserialize(cls, data):
        return cls(data)

traits = ["carnivore", "ambush", "burrowing", "climbing", "cooperation",
          "fat-tissue", "fertile", "foraging", "hard-shell", "herding",
          "horns", "long-neck", "pack-hunting", "scavenger", "symbiosis",
          "warning-call"]

trait_mapping = {trait.upper().replace("-", "_"): trait for trait in traits}

Trait = Enum(type=TraitSerialization, value="Trait", names=trait_mapping)
