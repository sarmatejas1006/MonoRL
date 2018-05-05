from RLClasses.action import Action
from RLClasses.observation import Observation


class EligibilityTrace(object):
    observation = Observation  # Observation
    action = Action  # Action
    value = None

    def __init__(self, o, a, v):
        self.observation = o
        self.action = a
        self.value = v
