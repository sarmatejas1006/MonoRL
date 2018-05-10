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


if __name__ == '__main__':
    s1 = ApplicationContext().get_instance()
    s2 = ApplicationContext().get_instance()

    if s1 == s2:
        print('singleton')
    else:
        print('Diff objects')



