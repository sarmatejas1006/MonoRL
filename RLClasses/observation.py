from RLClasses.obsArea import ObsArea
from RLClasses.obsFinance import ObsFinance
from RLClasses.obsPosition import ObsPosition


class Observation(object):
    area = ObsArea()
    position = ObsPosition()
    finance = ObsFinance()

    def __init__(self, pArea=area, pPosition=position, pFinance=finance):
        self.area = pArea
        self.position = pPosition
        self.finance = pFinance

    # Return a string representing the current observation
    def printInfo(self):
        info = ""  # string
        info += "Game Group Info\n"

        for i in range(10):
            for j in range(2):
                info += str(self.area.gameGroupInfo[i][j]) + " "
            info += "\n"

        info += "Position\n"
        info += str(self.position.relativePlayersArea) + "\n"

        info += "Finance" + "\n"
        info += "Relative Assets : " + str(self.finance.relativeAssets) + "\n"
        info += "Relative Money : " + str(self.finance.relativePlayersMoney) + "\n"

        return info
