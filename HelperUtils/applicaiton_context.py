import sys
sys.path.insert(0, "/Users/maitraikansal/PycharmProjects/MonoRL")
from RLHandlers.rlEnvironment import RLEnvironment
from MonopolyHandlers.initMethods import InitMethods


class ApplicationContext(object):

    def __init__(self):
        self.rlEnv = RLEnvironment()

    def get_instance(self):
        return self.rlEnv


if __name__ == '__main__':
    s1 = ApplicationContext().get_instance()
    s2 = ApplicationContext.get_instance()

    if s1 == s2:
        print('singleton')
    else:
        print('Diff objects')



