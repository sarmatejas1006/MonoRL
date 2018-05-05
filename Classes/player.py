class Player(object):

    def __init__(self):
        pass

    # ###### Region Fields ############

    # int
    id = None
    position = None
    name = None
    money = None

    # list
    propertiesPurchased = []
    mortgagedProperties = []
    buildingsBuilt = []

    # boolean
    inJail = None
    isAlive = None
    policyFrozen = None

    # Initialize current player' fields
    def agent_init(self, c, l, agentName, inputCount):
        pass

    # Receive the first observation of the game
    # No reward is expected now
    # Send an action back to the environment
    @staticmethod
    def agent_start(obs):
        return 0

    # Receive observation and reward and send an action back to the environment
    @staticmethod
    def agent_step(obs, reward):
        return 0

    # End of game
    def agent_end(self, reward):
        pass

    # End of experiment
    def agent_cleanup(self):
        pass

    # ###### Region HelperMethods  #############
    @staticmethod
    def getType():
        return 'r'

    # Get total number of houses
    def getTotalHouses(self):
        counter = 0
        for i in range(len(self.buildingsBuilt)):
            if 0 < self.buildingsBuilt[i] < 5:
                counter += 1
        return counter

    # Get total number of hotels
    def getTotalHotels(self):
        counter = 0
        for i in range(len(self.buildingsBuilt)):
            if self.buildingsBuilt[i] == 5:
                counter += 1
        return counter

    # Calculate payment for current position
    @staticmethod
    def getRentPayment(currentPosition):
        return 0

    # TODO
    # Set neural network
    def setNeural(self, network):
        pass

    # Get neural network
    # def getNeural(self):
    #     inputLayer = [None]*23
    #     outputLayer = [None]*100
    #     return [inputLayer, outputLayer]

    # save agent
    def saveOnFile(self, p):
        pass
