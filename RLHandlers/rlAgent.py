from Classes.player import Player
from RLClasses.observation import Observation
from RLClasses.obsArea import ObsArea
from random import random, randint
from RLClasses.eligibilityTrace import EligibilityTrace
from RLClasses.action import Action
from sklearn.neural_network import MLPClassifier


class RLAgent(Player):
    # ######### Region Fields #########
    # Last observation
    lastState = None
    lastAction = 0
    # Traces
    traces = []  # list of eligibility traces
    # Neural Network
    network = None
    # Current epoch - used only for training the nn
    currentEpoch = 0
    # RL - parameters
    epsilon = 0.0  # double
    alpha = 0.0  # double
    gamma = 0.0  # double
    lamda = 0.0  # double

    # Network input and Output
    X = None
    Y = None

    # Agent's type - random, qlearning or sarsa
    agentType = ""

    # ######### Region RLMethods #########

    # Initialize agent's parameters
    def agent_init(self, aType, policy, agentName, inputCount):
        # Initialize neural net
        self.network = MLPClassifier(activation='tanh', solver='sgd', alpha=1e-5, learning_rate=0.2, hidden_layer_sizes=150, random_state=1)
        # Not needed here

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

        # If agent not random
        if self.agentType != 'r':
            # Calculate Qvalues
            QValues = self.calculateQValues(observation)
            # Select final action based on the ε-greedy algorithm
            action = self.e_greedySelection(QValues)
            # Update local values
            self.lastAction = action
            self.lastState = observation

            self.traces.append(EligibilityTrace(observation, Action(action), 1))
        else:
            return self.randomAction()

    # Receive an observation and a reward from the environment and send the appropriate action
    def agent_step(self, observation, reward):
        # If this isn't a random agent calculate the Q values for every possible action
        action = 0
        if self.agentType != 'r':
            # Calculate Qvalues
            QValues = self.calculateQValues(observation)

            # Select action
            action = self.e_greedySelection(QValues)

            # If the policy of the agent isn't frozen then train the neural network
            if not self.policyFrozen:
                # If the agent is learning then update it's qValue for the selected action
                QValue = 0.0
                exists = False

                # Calculate the qValue either using the Q-learning or the SARSA algorithm
                if self.agentType == 'q':
                    exists = self.updateQTraces(observation, Action(action), reward)
                    QValue = self.Qlearning(self.lastState, Action(self.lastAction), observation, Action(self.findMaxValues(QValues)), reward)
                else:
                    exists = self.updateSTraces(observation, Action(action))
                    QValue = self.Sarsa(self.lastState, Action(self.lastAction), observation, Action(action), reward)

                # Train the NN
                self.trainNeural(self.createInput(self.lastState, self.lastAction), QValue)
                # Add trace to list
                if not exists:
                    self.traces.append(EligibilityTrace(self.lastState, Action(self.lastAction), 1))

            # Update local values
            self.lastAction = action
            self.lastState = observation

            return action
        # Else random action
        else:
            return self.randomAction()

    # End of current game
    def agent_end(self, reward):
        # Mark this agent as dead
        self.isAlive = False

        # If this isn't a random agent
        if self.agentType != 'r' and not self.policyFrozen:

            # Update Traces
            if self.agentType == 'q':
                self.updateQTraces(self.lastState, Action(self.lastAction), reward)
            else:
                # self.updateSTraces()
                pass

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

        # Add action
        inp = [float(action + 2) / 3.0]

        # Add every variable of the observation to the input list
        for k in range(len(observation.area.gameGroupInfo[0])):
            for kk in range(len(observation.area.gameGroupInfo[1])):
                inp.append(observation.area.gameGroupInfo[k, kk])

        inp.append(observation.finance.relativeAssets)
        inp.append(observation.finance.relativePlayersMoney)
        inp.append(observation.position.relativePlayersArea)

        # Return the input array
        return inp

    # Calculate payment for a specific property
    def getRentPayment(self, cp):
        pass

    # Return a random action for the current state
    def randomAction(self):
        i = int(randint(0, 10000) % 3)
        return i - 1

    # Initialize local parameters for a new game
    def initParams(self):
        if self.policyFrozen:
            self.alpha = 0
            self.epsilon = 0
            self.lamda = 0
            self.gamma = 0
        # numberOfProperties = 28
        # Initialize arrays
        Player.propertiesPurchased = [0] * 28
        Player.mortgagedProperties = [0] * 28
        Player.buildingsBuilt = [0] * 28

        self.agent_changeCurrentState(Observation)
        self.isAlive = True
        Player.inJail = False

        Player.money = 1500
        Player.position = 0

        self.lastAction = 0
        self.lastState = Observation

        self.traces = []  # list of traces

    # Change agent's current observation based on what the agent receives
    def agent_changeCurrentState(self, obs):
        self.lastState = obs

    # Train agent's neural network for specific input and desired output
    def trainNeural(self, inp, output):
        # Create the training sample for the neural network
        # Train nn
        self.network.fit(inp, [output])
        print("Epoch:", self.currentEpoch)

    # ε-greedy Selection Algorithm
    def e_greedySelection(self, QValues):
        # Create new action array
        actionSelected = 0

        # Calculate a new random value between 0-1
        val = random(0, 1)
        if val > self.epsilon:
            # Select best action
            actionSelected = self.findMaxValues(QValues)
        else:
            # Select random action
            actionSelected = self.randomAction()

        return actionSelected

    # Return the best value of a 2-d array. Ties are being broken randomly
    def findMaxValues(self, tempQ):
        # Create a new action and set the first qValue as max
        selectedValue = -1
        maxValue = tempQ[0]  # array

        # Search through the whole Q array to find the maximum value
        for i in range(len(tempQ)):
            if tempQ[i] > maxValue:
                selectedValue = i - 1
                maxValue = tempQ[i]
            # Break ties randomly
            elif tempQ[i] == maxValue:
                prValue = randint(1, 100)
                curValue = randint(1, 100)
                if curValue > prValue:
                    selectedValue = i - 1
                    maxValue = tempQ[i]

        return selectedValue

    # Q learning algorithm bestAction
    def Qlearning(self, p_lastState, p_lastAction, newState, bestAction, reward):
        QValue = self.network.predict(self.createInput(p_lastState, p_lastAction.action))[0]

        # run network for last state and last action
        previousQ = QValue

        # run network for new state and best action
        newQ = self.network.predict(self.createInput(newState, bestAction.action))[0]

        QValue += self.alpha * (reward + self.gamma * newQ - previousQ)
        return QValue

    # SARSA Algorithm
    def Sarsa(self, lastState, lastAction, newState, newAction, reward):
        QValue = self.network.predict(self.createInput(lastState, lastAction.action))[0]

        # run network for last state and last action
        previousQ = QValue

        # run network for new state and best action
        newQ = self.network.predict(self.createInput(newState, newAction.action))[0]

        QValue += self.alpha * (reward + self.gamma * newQ - previousQ)
        return QValue

    # Calculate network's output
    def calculateQValues(self, obs):
        tempQ = [] * 3
        for i in range(len(tempQ)):
            # Run network for action i,j to given observation
            tempQ[i] = self.network.predict(self.createInput(obs, i - 1))  # network output
        return tempQ

    # Update traces -- qlearning---Peng's Q(λ)
    def updateQTraces(self, obs, a, reward):
        found = False
        # Since the state space is huge we'll use a similarity function to decide whether two states are similar enough
        for i in range(len(self.traces)):
            if self.checkStateSimilarity(obs, self.traces[i].observation) and a.action == self.traces[i].action.action:
                self.traces[i].value = 0
                del self.traces[i]
                i -= 1

            elif self.checkStateSimilarity(obs, self.traces[i].observation) and a.action == self.traces[i].action.action:

                found = True

                self.traces[i].value = 1

                # Q[t] (s,a)
                qT = self.network.predict(self.createInput(self.traces[i].observation, self.traces[i].action.action))[0]

                # maxQ[t] (s[t+1],a)
                act = self.findMaxValues(self.calculateQValues(obs))
                maxQt = self.network.predict(self.createInput(obs, act))[0]

                # maxQ[t] (s[t],a)
                act = self.findMaxValues(self.calculateQValues(self.lastState))
                maxQ = self.network.predict(self.createInput(self.lastState, act))[0]

                # Q[t+1] (s,a) = Q[t] (s,a) + alpha * ( trace[i].value ) * ( reward + gamma * maxQ[t] (s[t+1],a) * maxQ[t] (s[t],a))
                qVal = qT + self.alpha * self.traces[i].value * (reward + self.gamma * maxQt - maxQ)
                self.trainNeural(self.createInput(self.traces[i].observation, self.traces[i].action.action), qVal)

            else:

                self.traces[i].value = self.gamma * self.lamda * self.traces[i].value

                # Q[t] (s,a)
                qT = self.network.predict(self.createInput(self.traces[i].observation, self.traces[i].action.action))[0]

                # maxQ[t] (s[t+1],a)
                act = self.findMaxValues(self.calculateQValues(obs))
                maxQt = self.network.predict(self.createInput(obs, act))[0]

                # maxQ[t] (s[t],a)
                act = self.findMaxValues(self.calculateQValues(self.lastState))
                maxQ = self.network.predict(self.createInput(self.lastState, act))[0]

                # Q[t+1] (s,a) = Q[t] (s,a) + alpha * ( trace[i].value ) * ( reward + gamma * maxQ[t] (s[t+1],a) * maxQ[t] (s[t],a))
                qVal = qT + self.alpha * self.traces[i].value * (reward + self.gamma * maxQt - maxQ)
                self.trainNeural(self.createInput(self.traces[i].observation, self.traces[i].action.action), qVal)

        return found

    # Update traces  -- sarsa
    def updateSTraces(self, obs, a):
        return False

    # Calculate similarity of states
    def checkStateSimilarity(self, obs1, obs2):

        similar = True

        # Check money similarity
        moneyDif = abs(obs1.finance.relativeAssets - obs2.finance.relativeAssets) + abs(obs1.finance.relativePlayersMoney - obs2.finance.relativePlayersMoney)
        if moneyDif >= 0.1:
            similar = False

        # Check area similarity
        if obs1.position.relativePlayersArea != obs2.position.relativePlayersArea:
            similar = False

        countDif = 0.0

        for i in range(len(obs1.area.gameGroupInfo[0])):
            if not similar:
                break
            countDif = 0
            for j in range(len(obs1.area.gameGroupInfo[1])):
                countDif = abs(obs1.area.gameGroupInfo[i][j] - obs2.area.gameGroupInfo[i][j])
                if countDif >= 0.1:
                    similar = False
                    break
        return similar
