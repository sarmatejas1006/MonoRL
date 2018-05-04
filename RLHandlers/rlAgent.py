from Classes.player import Player
from RLClasses.observation import Observation
from random import random


class RLAgent(Player):
    # ######### Region Fields #########
    # Last observation
    lastState = Observation()
    lastAction = None
    # Traces
    traces = []  # list of eligibility traces
    # Neural Network
    network = None
    # Current epoch - used only for training the nn
    currentEpoch = 0
    # RL - parameters
    epsilon = None  # double
    alpha = None  # double
    gamma = None  # double
    lamda = None  # double

    # Agent's type - random,qlearning or sarsa
    agentType = None

    # ######### Region RLMethods #########

    # Initialize agent's parameters
    def agent_init(self, aType, policy, agentName, inputCount):
        # Initialize neural net

        # ######### Region Initialize_parameters #########
        self.name = agentName
        self.id = None  # TODO add ID
        self.agentType = aType
        self.policyFrozen = policy

        if policy:
            self.epsilon = 0
            self.alpha = 0
        else:
            self.epsilon = 0.5
            self.alpha = 0.2

        self.gamma = 0.95
        self.lamda = 0.8

        self.currentEpoch = 1

        self.initParams()

    # First action of the agent, where no reward is to be expected from the environment
    def agent_start(self, observation):
        # Increase currentEpoch parameter ( used only in nn training)
        self.currentEpoch += 1

        # Initialize agent's parameters
        self.initParams()

        # Create new array for action
        action = 0

        # If agent not random
        # Calculate Qvalues
        # Select final action based on the ε-greedy algorithm
        # Update local values
        pass

    # Receive an observation and a reward from the environment and send the appropriate action
    def agent_step(self, observation, reward):
        # If this isn't a random agent calculate the Q values for every possible action
        action = 0
        # Calculate Qvalues
        # Select action
        # If the policy of the agent isn't frozen then train the neural network
        #   If the agent is learning then update it's qValue for the selected action
        #   Calculate the qValue either using the Q-learning or the SARSA algorithm
        # Add trace to list

        # Update local values
        # Else random action

    # End of current game
    def agent_end(self, reward):
        # Mark this agent as dead
        self.isAlive = False

        # If this isn't a random agent
        # TODO

        # Reduce RL-parameters values
        self.epsilon *= 0.99
        self.alpha *= 0.99

    # Occurs when the experiment ( total set of games ) is finished
    def agent_cleanup(self):
        # If this isn't a random agent and hasn't a frozen policy then store the agent to a file
        pass

    # Save network  on file
    def saveOnFile(self, path):
        pass

    # # ######### Region MiscMethods #########

    def getNeural(self):
        return self.network

    # Return type of agent
    def getType(self):
        return self.agentType

    # Set agent's neural network
    def setNeural(self, net):
        self.network = net

    # Create input for the neural network
    def createInput(self, observation, action):
        # TODO
        return [0]

    # Calculate payment for a specific property
    def getRentPayment(self, cp):
        pass

    # Return a random action for the current state
    def randomAction(self):
        pass

    # Initialize local parameters for a new game
    def initParams(self):
        if self.policyFrozen:
            self.alpha = 0
            self.epsilon = 0
            self.lamda = 0
            self.gamma = 0
        # numberOfProperties = 28
        # Initialize arrays
        super().propertiesPurchased = [0] * 28
        super().mortgagedProperties = [0] * 28
        super().buildingsBuilt = [0] * 28

        self.agent_changeCurrentState(Observation())
        self.isAlive = True
        super().inJail = False

        super().money = 1500
        super().position = 0

        self.lastAction = 0
        self.lastState = Observation()

        self.traces = []  # list of traces

    # Change agent's current observation based on what the agent receives
    def agent_changeCurrentState(self, obs):
        self.lastState = obs

    # Train agent's neural network for specific input and desired output
    def trainNeural(self, inp, output):
        # Create the training sample for the neural network
        # Train nn
        # TODO
        pass

    # ε-greedy Selection Algorithm
    def e_greedySelection(self, QValues):
        # Create new action array
        actionSelected = 0

        # Calculate a new random value between 0-1
        val = random(0, 1)
        if val > self.epsilon:
            # Select best action
            pass
        else:
            # Select random action
            pass

        return actionSelected

    # Return the best value of a 2-d array. Ties are being broken randomly
    def findMaxValues(self, tempQ):
        # Create a new action and set the first qValue as max
        selectedValue = -1
        maxValue = tempQ[0]  # array

        # Search through the whole Q array to find the maximum value
        # TODO

        return selectedValue

    # Q learning algorithmbestAction
    # TODO IMPORTANT!!!
    def Qlearning(self, p_lastState, p_lastAction, newState, bestAction, reward):
        QValue = 0.0

        # run network for last state and last action
        previousQ = QValue

        # run network for new state and best action
        newQ = 0.0

        QValue += self.alpha * (reward + self.gamma * newQ - previousQ)
        return QValue

    # SARSA Algorithm
    def Sarsa(self, lastState, lastAction, newState, newAction, reward):
        QValue = 0.0

        # run network for last state and last action
        previousQ = QValue

        # run network for new state and best action
        newQ = 0.0

        QValue += self.alpha * (reward + self.gamma * newQ - previousQ)
        return QValue

    # Calculate network's output
    def calculateQValues(self, obs):
        tempQ = []*3
        for i in range(len(tempQ)):
            # Run netowrk for action i,j to given observation
            input = self.createInput(obs, i - 1)
