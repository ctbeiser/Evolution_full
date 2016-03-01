import sys
import json

from feeding.test_species import SituationTestCase

data = sys.stdin.read()
situation = json.loads(data)

resolution = SituationTestCase.attackable_from_situation(situation)

print(json.dumps(resolution))
