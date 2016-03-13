"""

"""
from enum import Enum

HARD_SHELL_THRESHOLD = 4


traits = ["carnivore", "ambush", "burrowing", "climbing", "cooperation",
          "fat-tissue", "fertile", "foraging", "hard-shell", "herding",
          "horns", "long-neck", "pack-hunting", "scavenger", "symbiosis",
          "warning-call"]

trait_mapping = {trait.upper().replace("-", "_"): trait for trait in traits}

Trait = Enum("Trait", trait_mapping)