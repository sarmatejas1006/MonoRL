import sys
from RLHandlers.rlEnvironment import RLEnvironment


class ApplicationContext(object):

    rlEnv = RLEnvironment().get_instance()

    def __init__(self):
        pass

    def get_instance(self):

        if self.rlEnv is None:
            self.rlEnv = RLEnvironment().get_instance()

        return self.rlEnv





