import sys
sys.path.append("/Users/maitraikansal/PycharmProjects/MonoRL")
from RLHandlers.rlEnvironment import RLEnvironment


class ApplicationContext(object):

    rlEnv = RLEnvironment()

    def __init__(self):
        pass

    def get_instance(self):

        if self.rlEnv is None:
            self.rlEnv = RLEnvironment()

        return self.rlEnv





