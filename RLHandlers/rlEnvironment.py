import sys
sys.path.append("/Users/maitraikansal/PycharmProjects/MonoRL")
from RLClasses.actionMethods import ActionMethods
from Classes.player import Player
from Classes.board import Board
from random import shuffle
from Classes.commandCard import CommandCard
from RLClasses.observation import Observation
from RLClasses.obsPosition import ObsPosition
from RLClasses.obsArea import ObsArea
from RLClasses.obsFinance import ObsFinance
from RLHandlers.rlAgent import RLAgent
from HelperUtils.stopwatch import Stopwatch
import xml.etree.ElementTree as ET
from Classes.card import Card
from Classes.specialPositonCard import SpecialPositionCard
from Classes.propertyCard import PropertyCard
import os
import math
import random
import time


class RLEnvironment(object):

    rlEnv = None

    def __init__(self):
        pass

    def get_instance(self):

        if self.rlEnv is None:
            self.rlEnv = RLEnvironment()

        return self.rlEnv

    Awriter = open("actions.txt","w")

    # Handler for the helper methods of the project
    #initMethods = InitMethods()
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
    #methods =  ActionMethods(object)

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
    gamePlayers = []

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
    def addCard(self, pCard):
        if pCard not in self.gameCards:
            self.gameCards.append(pCard)

    def deleteCard(self, pCard):
        if pCard in self.gameCards:
            self.gameCards.remove(pCard)

    def createEnvInfo(self, pCard):
        # TODO
        return "info"

    # Create an instance of Observation to represent the current state of the environment
    def createObservation(self):

        obs = Observation(self.createArea(), self.createPosition(), self.createFinance())

        return obs

    # Create a new position instance based on the current game's data
    def createPosition(self):

        position = ObsPosition()

        relativePlayersArea = 0

        if (self.board.typeId[self.currentPosition] == 0) and (self.gamePlayers[self.currentPlayer].isAlive):

            relativePlayersArea = (self.getCardFromPosition(self.currentPosition).getGroup() + 1) / 10

        position.relativePlayersArea = relativePlayersArea

        return position

    # Create a new position instance based on the current game's data
    def createFinance(self):

        finance = ObsFinance()

        total = 0

        for i in range(len(self.gamePlayers)):
            total += self.methods.mActions.caclulateAllAssets(i)

        assets = self.methods.mActions.caclulateAllAssets(self.currentPlayer)

        # Current player's money / Total money
        finance.relativeAssets = assets / total
        finance.relativePlayersMoney = self.smoothFunction(self.gamePlayers[self.currentPlayer].money, 1500)

        return finance

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

                groupInfo.append([i,int(12 / len(self.gameCardsGroup[i].split(',')) * cPlayer)])
                groupInfo.append([i, int(12 / len(self.gameCardsGroup[i].split(',')) * oPlayers)])

                if groupInfo[i][1] == 12:

                    alivePlayers = 0
                    for k in range(self.currentPlayers):

                        if (self.gamePlayers[k].isAlive()) and (k != self.currentPlayer):
                            alivePlayers = alivePlayers + 1


                    groupInfo.append([i,int(groupInfo[i][1] / alivePlayers)])



            # If the group is completed
            else:

                gr = self.gameCardsGroup[i].split(',')
                mortCounter = 0

                tmp = self.buildings[int(self.gameCardsGroup[i].split(',')[len(self.gameCardsGroup[i].split(',')) - 1])]

                if self.completedGroups[i] == self.currentPlayer:

                    for j in range(len(gr)):

                        if self.gamePlayers[self.currentPlayer].mortgagedProperties[int(gr[j].ToString()).index()] == 1:
                            mortCounter = mortCounter +1



                groupInfo[i][1] = 0
                groupInfo[i][0] = 12 + tmp
                if mortCounter > 0:
                    groupInfo[i][0] = 12 - int(12 / len(self.gameCardsGroup[i].split(',')) * mortCounter)



                else:

                    groupInfo[i][0] = 0
                    groupInfo[i][1] = 12 + tmp



        for i in range(len(groupInfo[0])):

            for j in range(len(groupInfo[1])):

                    groupInfo[i][j] = float(groupInfo[i][j] / 17)

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
                            reward += self.buildings[i]



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

        return reward

    # Calculate reward in [-1, 1]
    def smoothFunction(self, x, factor):

        return (x / factor) / (1 + math.fabs(x / factor))


    # Convert degree to radian
    def DegreeToRadian(self, angle):

        return math.pi * angle / 180.0

    # Shuffle
    def shuffle(self, list):

        rng = random.randomint()
        n = list.Count
        while n > 1:

            n = n-1
            k = rng.Next(n + 1)
            value = list[k]
            list[k] = list[n]
            list[n] = value

        return list


    # Load an already created agent
    def NetworkloadNeural(self, path):
        # todo
        # return network
        pass
        return



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
        counter = 0

        for i in range(self.currentPosition):

            if i in self.propertyCardsPosition:
                counter = counter + 1

        return counter


    # Move current player on board
    def movePlayer(self, playerToMove):

        # System.Threading.Thread.Sleep(10)
        time.sleep(10)

        #Calculate the positions to move

        dice1 = random.randint(1,6)
        dice2 = random.randint(1,6)

        dice = dice1 + dice2

        if (self.currentPosition + dice) > 39:

            if dice != dice2:
                self.gamePlayers[playerToMove].money += 200
            else:

                if self.doublesInRow < 2:
                    self.gamePlayers[playerToMove].money += 200



            # Move the player
            currentPosition = self.gamePlayers[playerToMove].position + dice
            currentPosition = currentPosition % 40

            # Change current 's player current position
            self.gamePlayers[playerToMove].position = currentPosition

            if dice1 == dice2:
                self.doublesInRow = self.doublesInRow + 1
            else:
                self.doublesInRow = 0

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
                    counter = -1
                    for s in self.gameCardsGroup[1].split(','):
                        if self.properties[int(s)] == owner:
                            counter = counter + 1


                    amount = self.gameCards[self.getIndexFromPosition(self.currentPosition)].rent[counter]

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

    # Apply command card
    def onCommandCard(self):
        # Check whether it is a community chest card or a chance card
        if self.currentPosition in self.communityChestCardsPositions:

        # Take the 1st card of the list, apply it to the game and then move it to the last position
            self.applyCommandCard(self.communityChestCards[0])
            self.moveCommunityChestCard()

        else:
            # Take the !st card of the list, apply it to the game and then move it to the last position
            self.applyCommandCard(self.chanceCards[0])
            self.moveChanceCard()


    # Move 1st community chest card to the last position
    def moveCommunityChestCard(self):

        self.communityChestCards.Add(self.communityChestCards[0])
        self.communityChestCards.RemoveAt(0)

    # Move 1st chance card to the last position
    def moveChanceCard(self):
        self.chanceCards.Add(self.chanceCards[0])
        self.chanceCards.RemoveAt(0)

    # Apply a command card to the game state
    def applyCommandCard(self,commandCard):

        # Initially we check whether it's a fixed move or not
        if commandCard.fixedMove is not None:
            # Specify where we're gonna move the player
            moveTo = int(commandCard.fixedMove)
            # If the command card specifies him to collect money
            if commandCard.collect > 0:
                # Then if he passes through "GO" collect some money otherwise do nothing

                if moveTo - self.currentPosition <= 0:
                    self.gamePlayers[self.currentPlayer].money += commandCard.moneyTransaction
            # Change current position
            self.gamePlayers[self.currentPlayer].position = moveTo
            currentPosition = moveTo
            moved = True

        # Relative move
        elif commandCard.relativeMove is not None:
            # find the specific position to move
            # We'll move towards the nearest group
            if (int(commandCard.relativeMove)) > 0:
                moveTo = self.findNearestFromGroup(int(commandCard.relativeMove))

                # If the player is to collect money then add the specific amount to his balance
                if commandCard.collect > 0:

                    if moveTo - self.currentPosition <= 0:
                        self.gamePlayers[self.currentPlayer].money += commandCard.moneyTransaction


                # Change current position
                self.gamePlayers[self.currentPlayer].position = moveTo
                self.currentPosition = moveTo
                moved = True


        else:

            # If the player is to collect money
            if commandCard.collect > 0:

                # Check whether it is from the other players or from the bank
                if commandCard.playerInteraction > 0:
                    self.getMoneyFromPlayers(commandCard.moneyTransaction)

                else:
                    self.gamePlayers[self.currentPlayer].money += commandCard.moneyTransaction


            # Otherwise check whether he is to pay money
            if commandCard.collect == 0:

                # Calculate the total amount that his has to pay
                moneyToPay = commandCard.moneyTransaction + commandCard.houseMultFactor * self.gamePlayers[self.currentPlayer].getTotalHouses() + commandCard.hotelMultFactor * self.gamePlayers[self.currentPlayer].getTotalHotels()

                # Check wheter the player has the money to pay for his fine
                # If not then he has to declare bankruptchy and exit the game
                if self.methods.mActions.payMoney(self.currentPlayer, -1, moneyToPay) < 0:
                    # Remove him for the game
                    self.removePlayer(self.currentPlayer)
                    for i in range(self.gameCards):

                        if self.gamePlayers[self.currentPlayer].propertiesPurchased[i] == 1:

                            self.biddingWar(self.gameCards[i].getPosition())

    # Get money from every player other than the current and add them to his balance

    def getMoneyFromPlayers(self, p):

        for i in range(self.gamePlayers):

            if (i !=self.currentPlayer) and (self.gamePlayers[i].isAlive()):

                if self.methods.mActions.payMoney(i, self.currentPlayer, p) < 0:

                    # If the player can't pay then remove him from the game
                    self.removePlayer(i)
                    self.gamePlayers[self.currentPlayer].money += self.gamePlayers[i].money

                    for j in range(self.gamecards):
                        if self.gamePlayers[i].propertiesPurchased[j] == 1:

                            self.gamePlayers[self.currentPlayer].propertiesPurchased[j] = 1
                            self.properties[self.gameCards[j].getPosition()] = self.currentPlayer
                            if self.gamePlayers[i].mortgagedProperties[j] == 1:
                                self.gamePlayers[self.currentPlayer].mortgagedProperties[j] = 1
                                self.methods.mActions.checkIfCompleted(self.currentPlayer, self.gameCards[j].getPosition())

    # find nearest position that belongs to a specific group
    def findNearestFromGroup(self,p):
        moveTo = 0
        minDist = 100

        # Find the nearest utility to him amd move him there
        tmp = self.gameCardsGroup[p].split(',')
        for i in range(len(tmp)):
            if math.fabs(self.currentPosition - int(tmp[i])) < minDist:
                minDist = math.fabs(self.currentPosition - int(tmp[i]))
                moveTo = int(tmp[i])

        return moveTo

    # Act accordingly when a player lands on a special posotion on board
    def onSpecialPosition(self):

        # Special Position: {0, 4, 10, 20, 30, 38}

        # go
        if self.currentPosition == 0:
            pass

        # Income tax
        elif self.currentPosition == 4:
            # Pay either 10 % of income or 200 - whichever is lower

            minAmount = int(self.gamePlayers[self.currentPlayer].money * 0.1)
            if minAmount > 200:
                minAmount = 200

            if self.methods.mActions.payMoney(self.currentPlayer, -1, minAmount) < 0:

                # Remove him from the game
                self.removePlayer(self.currentPlayer)
                for i in range(self.gameCards):

                    if self.gamePlayers[self.currentPlayer].propertiesPurchased[i] == 1:

                        self.biddingWar(self.gameCards[i].getPosition())

        # Jail ( just visiting )
        elif self.currentPosition == 10:
            pass

        # FreeParking
        elif self.currentPosition == 20:
            pass

        # Jail Position
        elif self.currentPosition == 30:

            # Send him to jail
            self.gamePlayers[self.currentPlayer].position = 10
            self.gamePlayers[self.currentPlayer].inJail = True
            self.currentPosition = 10


        # Luxury tax
        else:

            if self.methods.mActions.payMoney(self.currentPlayer, -1, 75) < 0:

                # Remove him from game
                self.removePlayer(self.currentPlayer)
                for i in range(self.gameCards):

                    if self.gamePlayers[self.currentPlayer].propertiesPurchased[i] == 1:

                        self.biddingWar(self.gameCards[i].getPosition())

    # If the player is in jail then try to get out
    def inJailPosition(self):

        # System.Threading.Thread.Sleep(5)
        time.sleep(5)
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)

        # Get gim out of jail
        if dice1 == dice2:

            self.doublesInRow = 0
            self.getOutOfJailTries[self.currentPlayer] = 0
            self.gamePlayers[self.currentPlayer].inJail = False

        else:

            self.getOutOfJailTries[self.currentPlayer]=self.getOutOfJailTries[self.currentPlayer]+1
            if self.getOutOfJailTries[self.currentPlayer] < 3:
                self.env_selectNextAgent()


        # If maximum tries have been reached then pay the fine and get out normally
        if self.getOutOfJailTries[self.currentPlayer]==3:

            if self.methods.mActions.payMoney(self.currentPlayer, -1, 50) > 0:

                self.doublesInRow = 0
                self.getOutOfJailTries[self.currentPlayer] = 0
                self.gamePlayers[self.currentPlayer].inJail = False

            # Else remove him from game
            else:

                self.removePlayer(self.currentPlayer)
                for i in range(self.gameCards):

                    if self.gamePlayers[self.currentPlayer].propertiesPurchased[i]==1:

                        self.biddingWar(self.gameCards[i].getPosition())


                self.env_selectNextAgent()

        # If he isn't in jail then act as if it is a normal turn
        if not self.gamePlayers[self.currentPlayer].inJail:
            self.playGame()


    # Remove a player from the game
    def removePlayer(self,id):

        self.gamePlayers[id].agent_end(self.DEFEATREWARD)
        # Return hotels and houses to the bank
        self.currentHotels -= self.gamePlayers[id].getTotalHotels()
        self.currentHouses -= self.gamePlayers[id].getTotalHouses()

        for i in range(0,40):
            if self.properties[i]==id:
                self.properties[i] = -1
                self.buildings[i] = 0


        for i in range(len(self.completedGroups)):

            if self.completedGroups[i]==id:
                self.completedGroups[i] = -1


        # Have to attach player's neural net also
        self.getOutOfJailTries[id] = 0
        self.averageMoney[id] += self.gamePlayers[id].money

    # Initialize environment's parameters
    def env_init(self):

        # Create new list of agents
        self.gamePlayers = []
        self.currentPlayers = 3

        self.methods =  ActionMethods(self.get_instance())

        # Average money of every player during the game
        averageMoney = []

        # Start and play the game
        self.env_start()

        # Initialize agents.We 'll use the same for all games during this run
        for i in range(self.currentPlayers):

            self.gamePlayers.append(RLAgent(self.get_instance()))
            # System.Threading.Thread.Sleep(100)
            time.sleep(10)

            self.gamePlayers[i].agent_init('q', False, "Agent" + str(i), (23))
            #agent type(random-qlearning, policyFrozen, name, input vector length

            averageMoney.append(0)


        # Initialize stopwatch
        timer = Stopwatch()

        # Set total games
        self.totalGames = 1

        # Start the games
        for self.currentGame in range(self.totalGames):
            # System.Threading.Thread.Sleep(100)
            #time.sleep(10)

            self.Awriter.write("---------------------------------"+"\n")

            # Reset and start the timer
            timer.reset()
            #timer.start()

            # Initialize stepCounter variable to prevent it from going on forever and determine manually the winner
            self.stepCounter = 0

            # Start and play the game
            # self.env_start()

            if ((self.currentGame % 5)==0) and (self.gamePlayers[0].getType() != 'r'):
                self.gamePlayers[0].saveOnFile("agents/nn" + self.currentGame.to_string() + "games.dat")


        # Print experiment's info
        self.printInfo()

        # Close the writer
        self.textWriter.Close()

        # Cleanup agents
        self.env_cleanup()

        self.Awriter.Close()

    # Start playing the game
    def env_start(self):

        # System.Threading.Thread.Sleep(100)
        # time.sleep(100)

        # Start new game
        self.initGameParameters()

        # First player to play

        firstPlayer = random.randint(0,self.currentPlayers)

        # Play the first move of every agent
        for self.currentPlayer in range(self.currentPlayers):

            self.playFirstMoves((firstPlayer + self.currentPlayer) % self.currentPlayers)

        # Set the current player
        self.currentPlayer = firstPlayer

        # Start playing the game until it's finished
        while not self.env_gameIsOver():

            self.playGame()


        # End of game
        self.env_end()



    # Occurs when a game is finished
    def env_end(self):
        # Add moves
        self.moves.Add(self.stepCounter)

        # Stop the timer
        self.timer.stop()

        self.tmp = self.timer.ElapsedMilliseconds
        self.times.Add(self.tmp)
        found = False

        # Find the last alive agent and send his reward signal
        for i in range(self.gamePlayers):

            if self.gamePlayers[i].isAlive():
                found = True
                self.winners.Add(i)
                self.averageMoney[i] += self.gamePlayers[i].money
                self.gamePlayers[i].agent_end(self.WINREWARD)
                break

        if not found:
            self.winners.Add(-1)


    # Select next agent
    def env_selectNextAgent(self):


        # Check whether the maximum allowed number of steps has occurred
        # If so then end the game
        if self.stepCounter >= self.MAXSTEPS:

            # Declare all players as losers
            for i in range(self.gamePlayers):
                if self.gamePlayers[i].isAlive():

                    self.removePlayer(i)


            return


        # For some reason it's freaking freezing...
        # System.Threading.Thread.Sleep(15)
        time.sleep(15)

        # Since it's a new player he definately hasn't rolled any doubles yet
        self.doublesInRow = 0

        playersChecked = 0

        # Find the id of the next alive agent
        while not self.gamePlayers[self.currentPlayer].isAlive() and self.playersChecked <= self.currentPlayers:

            self.currentPlayer = self.currentPlayer+1
            self.currentPlayer = self.currentPlayer % self.currentPlayers
            playersChecked = playersChecked + 1


        # Increase his move counter since he's been selected
        self.playerMoves[self.currentPlayer] = self.playerMoves[self.currentPlayer] + 1

        self.stepCounter = self.stepCounter + 1


    # Specify whether the game is over
    def env_gameIsOver(self):

        # Count how many players are still alive in the game

        counter = 0
        for i in range(self.gamePlayers):

            if self.gamePlayers[i].isAlive():
                counter = counter + 1


            # If there are more than one player then the game isn't over yet
            if counter > 1:
                return False
            else:
                return True


    # Clean up memory when the experiment is completed
    def env_cleanup(self):

        # Print average money of every player
        averageMoneyWriter = open("txt/AverageMoney.txt")

        for i in range(self.currentPlayers):
            averageMoneyWriter.WriteLine((self.averageMoney[i] / self.totalGames).ToString())

        averageMoneyWriter.Close()

        # Dispose agent and save neural networks

        for i in range(self.currentPlayers):

            self.gamePlayers[i].saveOnFile("agents/nnFinalNeural--" + str(i) + ".dat")
            self.gamePlayers[i].agent_cleanup()

        print('Experiment finished')
        # MessageBox.Show("Experiment finished")

    # Initiliaze game parameters
    def initGameParameters(self):

        self.chanceCards = []
        self.communityChestCards = []

        self.gameCards = []
        self.gameCommandCards = []

        self.currentHotels = 0
        self.currentHouses = 0

        self.currentPosition = 0
        self.currentPlayer = 0

        self.doublesInRow = 0

        board = Board()

        # Both CommandCards and PropertyCards implement the Card interface
        # Set Command Cards(both Community Chest and Chance cards )
        self.initialiseCommandCards()

        # Set Property Cards
        self.initialisePropertyCards()

        # Create information for every position on board
        self.initialiseBoard()

        self.getOutOfJailTries = []
        self.playerMoves = []

        # Initialize arrays
        for i in range(len(self.properties)):
            self.properties[i] = -1
            self.buildings[i] = 0

            # Initialize array
            for i in range(len(self.gameCardsGroup)):
                self.completedGroups[i] = -1

            for i in range(len(self.gamePlayers)):
                self.getOutOfJailTries.append(0)
                self.playerMoves.append(1)


    # Play first move of the game
    def playFirstMoves(self,i):
        # move the current player
        self.movePlayer(i)
        group = -1

        if self.board.typeId[self.currentPosition] == 0:
            group = self.getCardFromPosition(self.currentPosition).getGroup()


        # Create an instance of the observation class
        obs = self.createObservation()

        # Integer array to specify the actions

        action = 0
        # Pause thread
        # System.Threading.Thread.Sleep(15)
        time.sleep(15)

        # If the current player is agent then sent him a message
        action = self.gamePlayers[self.currentPlayer].agent_start(obs)

        actions = {action, group}

        if group >= 0:
            self.methods.receiveAction(actions)

        self.gamePlayers[self.currentPlayer].position = self.currentPosition


    # Play the game
    def playGame(self):

        # Check whether the player is alive
        if self.gamePlayers[self.currentPlayer].isAlive:

            self.currentPosition = self.gamePlayers[self.currentPlayer].position

            # Move player only if not in prison
            if self.gamePlayers[self.currentPlayer].inJail:
                self.inJailPosition()
            else:

                self.movePlayer(self.currentPlayer)

                # If he throws 3 times doubles in a row then send him to jail
                if self.doublesInRow == 3:

                    # Send him to jail
                    self.gamePlayers[self.currentPlayer].position = 10
                    self.gamePlayers[self.currentPlayer].inJail = True
                    self.currentPosition = 10
                    self.doublesInRow = 0

                    # if he goes to jail then select the next agent
                    self.env_selectNextAgent()

                else:
                    self.moved = True

                    # While the player hasn't moved from a command card and his is still alive ( in case he has paid something)
                    while (self.moved and self.gamePlayers[self.currentPlayer].isAlive) and (not self.gamePlayers[self.currentPlayer].inJail):

                        # Check where he landed
                        self.onPositionChanged()

                        self.moved = False

                        # Check whether he is in a special position or command card
                        if self.currentPosition in self.specialPositions:
                            self.onSpecialPosition()
                        elif (self.currentPosition in self.chanceCardsPositions) or (self.currentPosition in self.communityChestCardsPositions):
                            self.onCommandCard()


                    # If the player is still alive then procceed with the action selected
                    if (self.gamePlayers[self.currentPlayer].isAlive) and (not self.gamePlayers[self.currentPlayer].inJail):

                        tempPosition = self.currentPosition
                        while self.board.typeId[tempPosition] !=0 :
                            tempPosition = tempPosition + 1

                    group = self.getCardFromPosition(tempPosition).getGroup()

                    # List of actions
                    getList = []
                    spendList = []

                    for currentGroup in range(len(self.gameCardsGroup)):

                        group = self.getCardFromPosition(tempPosition).getGroup()
                        group = (group + currentGroup) % len(self.gameCardsGroup)

                    # check whether a player can act on a specific group
                    ableToAct = False
                    for i in range(len(self.gameCardsGroup.split(','))):
                        if self.properties[int(self.gameCardsGroup[group].split(',')[i])] == self.currentPlayer:
                            ableToAct = True

                        if int(self.gameCardsGroup[group].split(',')[i]) == self.currentPosition:

                            if (self.properties[self.currentPosition] == self.currentPlayer) or (self.properties[self.currentPosition] == -1):
                                ableToAct = True

                    # endregion CheckAbilityToAct

                    if ableToAct:

                        # Integer to specify the action
                        action = 0

                        # Pause thread
                        # System.Threading.Thread.Sleep(20)
                        time.sleep(20)

                        # Create an instance of the observation class

                        obs = self.createObservation()

                        # region ChangeCurrentObservation
                        obs.position.relativePlayersArea = float((group + 1) / 10)

                        # endregion ChangeCurrentObservation

                        action = self.gamePlayers[self.currentPlayer].agent_step(obs, self.calculateReward(self.currentPlayer))

                        if self.currentPlayer == 0:
                            self.Awriter.write(action.ToString() + " -- " + group.ToString())

                            if action == 0:
                                set = {action, group}
                            if action > 0:
                                spendList.Add(set)
                            else:
                                getList.Add(set)

                        for i in range(getList):

                            # System.Threading.Thread.Sleep(5)
                            time.sleep(5)
                            self.methods.receiveAction(getList[i])

                        for i in range(spendList):
                            # System.Threading.Thread.Sleep(5)
                            time.sleep(5)
                            self.methods.receiveAction(spendList[i])


                        # If current property isn't owned yet start the bidding game
                        if (self.properties[self.currentPosition] == -1) and (self.board.typeId[self.currentPosition]==0):

                            self.biddingWar(self.currentPosition)


                            # If he hasn't thrown doubles then select the next agent
                            if self.doublesInRow == 0:
                                self.env_selectNextAgent()


                        # If he is either dead or in jail select next agent
                        else:

                            self.env_selectNextAgent()

                    # If he isn't alive then select the next alive agent
                    else:
                        self.env_selectNextAgent()



    # Start the bidding
    def biddingWar(self,currentPosition):

        if (self.properties[self.currentPosition] == -1) and (self.board.typeId[self.currentPosition] == 0):

            # Find the group of the current card
            group = self.getCardFromPosition(self.currentPosition).getGroup()

            # Start the bidding war until some player has outbid everyone else

            higherBidder = -1
            totalBidders = 0
            multFactor = 0.4
            finished = False
            maxBid = 0

        while not finished:

            bid = int(multFactor * self.getCardFromPosition(self.currentPosition).getValue())

            for i in range(self.currentPlayers):
                if self.gamePlayers[i].isAlive:
                    # Pause thread
                    # System.Threading.Thread.Sleep(20)
                    time.sleep(20)

                    specObs = self.createObservation()

                    # region RelativeAssets

                    total = 0

                    for j in range(self.gamePlayers):

                        total += self.methods.mActions.caclulateAllAssets(j)


                    total += self.getCardFromPosition(currentPosition).getMortgageValue() - bid

                    assets = self.methods.mActions.caclulateAllAssets(i) + self.getCardFromPosition(self.currentPosition).getMortgageValue() - bid

                    # Current player's money / Total money
                    specObs.finance.relativeAssets = assets / total

                    # Current player's money / Total money
                    specObs.finance.relativePlayersMoney = self.smoothFunction(self.gamePlayers[i].money - bid, 1500)

                    # Relative players position
                    specObs.position.relativePlayersArea = (group + 1) / 10

                    specObs.area.gameGroupInfo[group, 0] += (self.gameCardsGroup[group].Split(',').Length / 12) / 17


                    action = self.gamePlayers[i].agent_step(specObs, self.calculateReward(i))

                    if i == 0:
                        # Remove comment
                        self.Awriter.write("BiddingTime " + action.ToString() + " -- " + group.ToString())

                    if (action > 0) and (self.gamePlayers[i].money >= bid):

                        higherBidder = i
                        totalBidders = totalBidders + 1
                        maxBid = bid


            if totalBidders > 1:
                finished = False
                higherBidder = -1
                multFactor += 0.2
                totalBidders = 0

            elif totalBidders == 0:

                higherBidder = -1
                finished = True

            else:
                finished = True


        # If someone is chosen as a higher bidder then make him buy the current property
        if higherBidder != -1:

            self.properties[self.currentPosition] = higherBidder
            self.gamePlayers[higherBidder].propertiesPurchased[self.getIndexFromPosition(self.currentPosition)] = 1
            self.gamePlayers[higherBidder].money -= maxBid
            self.methods.mActions.checkIfCompleted(higherBidder, self.currentPosition)

    # set command card after parsing data from xml file
    def initialiseCommandCards(self):

        try:
            # XML reader to store the commandCards
            if os.path.isfile('/Users/maitraikansal/PycharmProjects/MonoRl/Data/CommandCards.xml'):

                tree = ET.parse('/Users/maitraikansal/PycharmProjects/MonoRl/Data/CommandCards.xml')
                root_node = tree.getroot()

                for node in root_node:
                    p_card = CommandCard(node.find('TypeOfCard').text, node.find('Text').text, node.find('FixedMove').text,
                                          node.find('Collect').text, node.find('MoneyTransaction').text, node.find('PlayersInteraction').text,
                                          node.find('HouseMultFactor').text, node.find('HotelMultFactor').text)
                    self.addCommandCard(p_card)

                    self.setCommandCards()

        except Exception as e:
            print('Exception encountered: ', str(e))
            return False

        return True

    # set Property card after parsing data from xml file
    def initialisePropertyCards(self):
        try:
            # XML reader to store the commandCards
            if os.path.isfile('/Users/maitraikansal/PycharmProjects/MonoRl/Data/Properties.xml'):

                tree = ET.parse('/Users/maitraikansal/PycharmProjects/MonoRl/Data/Properties.xml')
                root_node = tree.getroot()

                for node in root_node:
                    rent = []
                    rentString = node.find('Rent').text.split(',')
                    for s in rentString:
                        rent.append(int(s));

                    p_card = PropertyCard(node.find('Name').text, node.find('Position').text,
                                          node.find('Price').text,
                                          rent,
                                          node.find('Mortage').text,
                                          node.find('HouseCost').text,
                                          node.find('HotelCost').text, node.find('Group').text)

                    self.addCard(p_card)
                    #self.setCards()

        except Exception as e:
            print('Exception encountered: ', str(e))
            return False

        return True

    def initialiseBoard(self):

        b = [Card() for i in range(40)]  # empty card array
        t = [-1] * 40  # int array of -1

        # Add PropertyCards

        for i in range(len(self.getCards())):
           b[int(self.getCards()[i].getPosition())] = self.getCards()[i]
           t[int(self.getCards()[i].getPosition())] = 0

        # Add CommunityChestCards

        for i in range(len(self.getCommunityCardPositions())):
            b[int(self.getCommunityCardPositions()[i])] = CommandCard()
            t[int(self.getCommunityCardPositions()[i])] = 1

        # Add ChanceCards
        for i in range(len(self.getChanceCardPositions())):
            b[int(self.getChanceCardPositions()[i])] = CommandCard()
            t[int(self.getChanceCardPositions()[i])] = 2



        # Specify that every position left on board is a special position ( GO, Jail, etc... )
        # We'll take care of what occurs on every case in a different method
        for i in range(len(b)):
            if t[i] < 0:
                t[i] = 3
                b[i] = SpecialPositionCard()

        # Set the global board parameter
        self.setBoard(Board(b, t))

    # Print experiment's info
    def printInfo(self):

        # Check whether the directory exists or not
        if not os.path.exists("txt/"):
            os.makedirs("txt/")

        # Create streamwriter for the output file
        textWriter = open("txt/output.txt")
        winner = open("txt/winners.txt")
        move = open("txt/moves.txt")

        textWriter.write("=========== MONORL TEST RUN =============")
        for i in range(len(self.winners)):

            textWriter.write(
            str(i + 1) + "        " + str(self.times[i] / 1000)+ "        " + self.winners[
                i] + "        " + str(self.moves[i]))
            winner.write(str(self.winners[i]))
            move.write(str(self.moves[i]))

            textWriter.write("Game:", i + 1, "Winner:", str(self.winners[i]), "Moves:", str(self.moves[i]))

        winner.close()


if __name__ == "__main__":
    RLEnvironment().get_instance().env_init()
    RLEnvironment().get_instance().playGame()







