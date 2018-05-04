from MonopolyHandlers.initMethods import InitMethods
from RLClasses.actionMethods import ActionMethods
from Classes.player import Player
from random import shuffle
from Classes.propertyCard import PropertyCard
from Classes.commandCard import CommandCard
import time


class RLEnvironment:
    Awriter = "actions.txt"

    # Handler for the helper methods of the project
    initMethods = InitMethods()
    # ######### Region Private Fields #########
    # List of winners of every game
    winners = []

    # List of the duration of every game
    times = []

    # List of moves of every game
    moves = []

    # Average money of every player
    averageMoney = []

    # Stopwatch timer to calculate duration of game
    timer = None

    # Int value specifying the current value
    currentGame = 0

    # Int array specifying the times that each player played during a game
    playerMoves = []

    # Rounds for every game before it ends
    stepCounter = 0

    # Total number of games
    totalGames = 0

    # Action methods
    methods = ActionMethods()

    # Current player and current position value
    currentPlayer = 0
    currentPosition = 0

    moved = False

    # Jail-helper variables
    doublesInRow = 0
    getOutOfJailTries = []

    # int[] properties = ( default = -1 , otherwise the index of the player )
    properties = [0] * 40

    # int[] buildings = the number of buildings on each position on the board
    buildings = [None] * 40

    # int[] completedGroups = (default = -1, otherwise the index of the player )
    completedGroups = [0] * 10

    # Specify the color of each group of cards ( i.e. 1st group - Dark Blue )
    # #{'dark_blue': '#053057', 'purple': '#800080', 'violet': '#774177',
    #                    'orange': '#FF8D00', 'red': '#B20000', 'yellow': '#FFDB00',
    #                    'blue': '#0AAFDF', 'black': '#000000', 'white': '#ffffff'}
    groupCardColour = ['#053057', '#800080', '#774177', '#FF8D00', '#B20000', '#FFDB00', '#0AAFDF', '#000000', '#ffffff']

    # Exact Position of Command Cards and Special Positions (as Jail,Go,Tax etc) on board
    # We'll use these variables later to create the board and specify the type of each position
    propertyCardsPosition = list(range(1, 40))
    communityChestCardsPositions = [2, 17, 33]
    chanceCardsPositions = [7, 22, 36]
    specialPositions = [0, 4, 10, 20, 30, 38]

    # List of all the property cards of game
    gameCards = []

    # List of string that contain the positions on board that create a group
    # i.e. the value "1,3" -> the 1st and 3rd position of board form a group
    gameCardsGroup = ["12,28", "5,15,25,35", "1,3", "6,8,9", "11,13,14", "16,18,19", "21,23,24", "26,27,29", "31,32,34", "37,39"]

    # List of Game Players
    gamePlayers = [Player()]

    # List of CommandCards (both Community Chest and Chance cards)
    gameCommandCards = [CommandCard]

    # Specific sub-lists of CommandCards.
    # When a player takes a card then it goes to the last index of the list and all the rest
    # move one position to the left.
    communityChestCards = [CommandCard]
    chanceCards = [CommandCard]

    # Variable to determine the current state of the game ( for comparison with the const values mentioned above).
    currentHouses = []
    currentHotels = []
    currentPlayers = []

    # Board variable that specifies the card on every position and it's type ( as described on Board.cs)
    board = None

    # Global const values
    MAXPLAYERS = 4
    MAXHOUSES = 25
    MAXHOTELS = 10
    MAXAGENTACTIONS = 3
    MAXSTEPS = 2000
    REWARD = 0
    WINREWARD = 10
    DEFEATREWARD = -10

    # Const value to calculate the sin of every position on board
    sinConst = 4.61538

    # ##### Region SetMethods #######
    # Set the board variable ( represents info for every position of the board)
    def setBoard(self, b):
        self.board = b

    # Create lists of Chance and Community Chest Cards depending on the type of the card that we get from the xml file
    def setCommandCards(self):
        for i in range(len(self.gameCommandCards)):
            if self.gameCommandCards[i].getType() > 0:
                self.chanceCards.append(self.gameCommandCards[i])
            else:
                self.communityChestCards.append(self.gameCommandCards[i])

        # Shuffle cards
        self.chanceCards = shuffle(self.chanceCards)
        self.communityChestCards = shuffle(self.communityChestCards)

    # ##### Region GetMethods #######
    # Get maximum hotels
    def getMaxHotels(self):
        return self.MAXHOTELS

    # Get maximum houses
    def getMaxHouses(self):
        return self.MAXHOUSES

    # Get the colour of a group
    def getColour(self, pName):
        i = 0
        for c in self.gameCards:
            if c.getName() == pName:
                i = c.getGroup()
        return self.groupCardColour[i]

    # Get specific positions of CommandCards

