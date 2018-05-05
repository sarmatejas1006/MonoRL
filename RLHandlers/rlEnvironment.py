from MonopolyHandlers.initMethods import InitMethods
from RLClasses.actionMethods import ActionMethods
from Classes.player import Player
from random import shuffle
from Classes.propertyCard import PropertyCard
from Classes.commandCard import CommandCard
from RLClasses.observation import Observation
from RLClasses.obsPosition import ObsPosition
from RLClasses.obsArea import ObsArea
from RLClasses.obsFinance import ObsFinance
import time
import math
import random


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

    # Get specific positions of CommandCard

    def getCommunityCardPositions(self):

        return self.communityChestCardsPositions

    def getChanceCardPositions(self):

        return self.chanceCardsPositions

    # Get Game Property Cards
    def getCards(self):

        return self.gameCards

    # Get Game Command Cards
    def getCommandCards(self):

        return self.gameCommandCards

    # Get Game Players
    def getPlayers(self):

        return self.gamePlayers

    # Get maximum actions available
    def getMaxActions(self):

        return self.MAXAGENTACTIONS

    # Method to add and delete a CommandCard
    def addCommandCard(self, pCard):
        if pCard not in self.gameCommandCards:
            self.gameCommandCards.append(pCard)

    def deleteCommandCard(self,pCard):
        if pCard in self.gameCommandCards:
            self.gameCommandCards.remove(pCard)

    # Method to add and delete a PropertyCard
    def addCommandCard(self, pCard):
        if pCard not in self.gameCards:
            self.gameCards.append(pCard)

    def deleteCommandCard(self, pCard):
        if pCard in self.gameCards:
            self.gameCards.remove(pCard)

    def createEnvInfo(self, pCard):
        #TODO

     # Create an instance of Observation to represent the current state of the environment
    def createObservation(self):

        obs = Observation(self.createArea(), self.createPosition(), self.createFinance());

        return obs

    # Create a new position instance based on the current game's data
    def createPosition(self):

        position = ObsPosition()

        relativePlayersArea = 0

        if self.board.typeId[self.currentPosition].Equals(0) and self.gamePlayers[self.currentPlayer].isAlive:

            relativePlayersArea = (self.getCardFromPosition(self.currentPosition).getGroup() + 1) / 10

        position.relativePlayersArea = relativePlayersArea

        return position

    # Create a new position instance based on the current game's data
    def createFinance(self):

        finance = ObsFinance()

        total = 0;

        for i in range(len(self.gamePlayers)):
            total += self.methods.mActions.caclulateAllAssets(i)

        assets = self.methods.mActions.caclulateAllAssets(self.currentPlayer)

        # Current player's money / Total money
        finance.relativeAssets = assets / total
        finance.relativePlayersMoney = self.smoothFunction(self.gamePlayers[self.currentPlayer].money, 1500);

        return finance;

    # create a new area instance based on the current game's data
    def createArea(self):

        area = ObsArea()

        groupInfo = []
        for i in range(len(self.gameCardsGroup)):

            # Group isn't completed
            if self.completedGroups[i] == -1:

                cPlayer = 0
                oPlayers = 0

                tmp = self.gameCardsGroup[i].split(',')

                for j in range(len(tmp)):

                    if self.properties[int(tmp[j])]==self.currentPlayer:

                        if self.gamePlayers[self.currentPlayer].mortgagedProperties[int(tmp[j]).index()]==0:
                            cPlayer = cPlayer + 1


                        elif self.properties[int(tmp[j])] != -1:
                            oPlayer = oPlayer + 1


                        groupInfo[i, 0] = int(12 / len(self.gameCardsGroup[i].split(',')) * cPlayer)
                        groupInfo[i, 1] = int(12 / len(self.gameCardsGroup[i].split(',')) * oPlayers)

                        if groupInfo[i, 1] == 12:

                            alivePlayers = 0;
                            for k in range(self.currentPlayers):

                                if (self.gamePlayers[k].isAlive()) and (k != self.currentPlayer):
                                    alivePlayers = alivePlayers + 1


                            groupInfo[i, 1] = int(groupInfo[i, 1] / alivePlayers)



            # If the group is completed
            else:

                gr = self.gameCardsGroup[i].split(',')
                mortCounter = 0;

                tmp = self.buildings[int(self.gameCardsGroup[i].split(',')[len(self.gameCardsGroup[i].split(',')) - 1])]

                if self.completedGroups[i] == self.currentPlayer:

                    for j in range(len(gr)):

                    if self.gamePlayers[self.currentPlayer].mortgagedProperties[int(gr[j].ToString()).index()] == 1:
                        mortCounter = mortCounter +1



                groupInfo[i, 1] = 0;
                groupInfo[i, 0] = 12 + tmp;
                if mortCounter > 0:
                    groupInfo[i, 0] = 12 - int(12 / len(self.gameCardsGroup[i].split(',')) * mortCounter);



                else:

                    groupInfo[i, 0] = 0;
                    groupInfo[i, 1] = 12 + tmp;



        for i in range(len(groupInfo[0])):

            for j in range(len(groupInfo[1])):

                    groupInfo[i, j] = float(groupInfo[i, j] / 17)

        area.gameGroupInfo = groupInfo

        return area

    def calculateReward(self, player):

        reward = 0
        for i in range(len(self.properties)):

            if self.board.typeId[i] == 0:

                if self.properties[i] == player:

                    if self.gamePlayers[player].mortgagedProperties[i.index()] == 0:
                        reward  = reward + 1
                        if self.buildings[i] > 0:
                            reward += self.buildings[i];



                elif self.properties[i] == -1:

                    reward = reward - 1
                    if self.buildings[i] > 0:
                        reward -= self.buildings[i]




        for i in range(len(self.completedGroups)):

            if self.completedGroups[i] == player:

                reward += (i + 1)

            elif self.completedGroups[i] != -1:
                reward -= (i + 1)

        total = 0
        assetFactor = 0
        alivePlayers = 0
        for i in range(self.currentPlayers):

            if self.gamePlayers[i].isAlive():

                alivePlayers = alivePlayers +1
                total += self.gamePlayers[i].money
                if i == player:
                    assetFactor = self.gamePlayers[i].money



        assetFactor = assetFactor / total

        reward = self.smoothFunction(reward, alivePlayers * 5)

        reward = reward + (1 / alivePlayers) * assetFactor

        return reward;

    # Calculate reward in [-1, 1]
    def smoothFunction(self, x, factor):

        return (x / factor) / (1 + math.fabs(x / factor))


    # Convert degree to radian
    def DegreeToRadian(self, angle):

        return math.pi * angle / 180.0

    # Shuffle
    def shuffle(self, list):

        rng = random.randomint()
        n = list.Count;
        while n > 1:

            n = n-1
            k = rng.Next(n + 1)
            value = list[k]
            list[k] = list[n]
            list[n] = value

        return list


    # Load an already created agent
    def NetworkloadNeural(self, path):

        pass #todo

    return network



    # Load an already created agent
    def loadAgent(self, path):
        #todo
        pass
    # Get card from position
    def getCardFromPosition(self, currentPosition):

        # Count all the number of property cards that are between the start of the
        # board and player's current position
        return self.gameCards[currentPosition.index()]


    # Get index from position
    def getIndexFromPosition(self,  currentPosition):

        # Count all the number of property cards that are between the start of the
        # board and player's current position
        counter = 0;

        for i in range(self.currentPosition):

            if i in self.propertyCardsPosition:
                counter = counter + 1

        return counter


    # Move current player on board
    def movePlayer(self, playerToMove):

        System.Threading.Thread.Sleep(10);

        #Calculate the positions to move
        rnd = random.randint(1,100)
        dice1 = rnd.Next(1, 10000) % 6 + 1;
        dice2 = rnd.Next(1, 10000) % 6 + 1;

        dice = dice1 + dice2;

        if (self.currentPosition + dice) > 39:

            if dice != dice2:
                self.gamePlayers[playerToMove].money += 200;
            else:

                if self.doublesInRow < 2:
                    self.gamePlayers[playerToMove].money += 200;



            # Move the player
            currentPosition = self.gamePlayers[playerToMove].position + dice;
            currentPosition = currentPosition % 40;

            # Change current 's player current position
            self.gamePlayers[playerToMove].position = currentPosition;

            if dice1 == dice2:
                self.doublesInRow = self.doublesInRow + 1
            else:
                self.doublesInRow = 0;

    # Check whether the user has to pay rent for the current property
    def onPositionChanged(self):

        # Check whether the current position is a property card
        if self.board.typeId[self.currentPosition] == 0:

            # If it is then check whehter it is in someone's possession
            if self.properties[self.currentPosition] != -1 or self.properties[self.currentPosition] == self.currentPlayer:
                owner = self.properties[self.currentPosition]

                # If the player has mortgaged the area then pay nothing
                if self.gamePlayers[owner].mortgagedProperties[self.getIndexFromPosition(self.currentPosition)] == 1:
                    return

                amount = self.gamePlayers[owner].getRentPayment(self.getIndexFromPosition(self.currentPosition))

                if self.getCardFromPosition(self.currentPosition).getGroup() > 1:

                    if (self.completedGroups[self.getCardFromPosition(self.currentPosition).getGroup()] == owner) and (self.buildings[self.currentPosition] == 0):
                            amount *= 2

                # Utility
                if self.getCardFromPosition(self.currentPosition).getGroup() == 0:
                    rnd = random.randint(1,100)
                amount = amount * (rnd.Next(1, 7) + rnd.Next(1, 7))


                # Railway
                if self.getCardFromPosition(self.currentPosition).getGroup() == 1:
                    counter = -1;
                    for s in self.gameCardsGroup[1].split(','):
                        if self.properties[int(s)] == owner:
                            counter = counter + 1


                    amount = self.gameCards[selg.getIndexFromPosition(self.currentPosition)].rent[counter]

                    if self.methods.mActions.payMoney(self.currentPlayer, owner, int(amount)) < 0:

                    # If the player can't pay then remove him from the game
                    self.removePlayer(self.currentPlayer)
                    self.gamePlayers[owner].money += self.gamePlayers[self.currentPlayer].money
                    for i in range(len(self.gameCards)):

                        if self.gamePlayers[self.currentPlayer].propertiesPurchased[i] == 1:

                    self.gamePlayers[owner].propertiesPurchased[i] = 1
                    self.properties[self.gameCards[i].getPosition()] = owner
                    if self.gamePlayers[self.currentPlayer].mortgagedProperties[i] == 1:
                        self.gamePlayers[owner].mortgagedProperties[i] = 1
                    self.methods.mActions.checkIfCompleted(owner, self.gameCards[i].getPosition())




