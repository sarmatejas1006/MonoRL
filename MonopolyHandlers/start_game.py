import sys
sys.path.append("/Users/maitraikansal/PycharmProjects/MonoRL")
from HelperUtils.applicaiton_context import ApplicationContext


class StartGame(object):

    def initiate_game(self):\

        ApplicationContext().get_instance().env_init()
        ApplicationContext().get_instance().playGame()


if __name__ == "__main__":
    StartGame().initiate_game()


