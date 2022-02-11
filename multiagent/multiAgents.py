# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util
from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        newFoodPos = newFood.asList()
        newFoodDistance = [manhattanDistance(xy, newPos) for xy in newFoodPos]
        newGhostPos = [s.getPosition() for s in newGhostStates]
        ghostDistance = []
        for i in range(len(newGhostStates)):
            if newScaredTimes[i] == 0:
                ghostDistance.append(manhattanDistance(newGhostPos[i], newPos))
        if len(ghostDistance) > 0:
            minGhostDistance = min(ghostDistance)
        else:
            minGhostDistance = 0
        if len(newFoodDistance) > 0:
            minFoodDistance = min(newFoodDistance)
            sumFoodDistance = sum(newFoodDistance) / len(newFoodDistance)
        else:
            minFoodDistance = 0
            sumFoodDistance = 0
        foodCount = successorGameState.getNumFood()
        if 0 < minGhostDistance < 3:
            return - minFoodDistance - foodCount * 15 + minGhostDistance
        return - minFoodDistance - sumFoodDistance - foodCount * 20 + minGhostDistance

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        ghostNumber = gameState.getNumAgents() - 1
        return self.maximize(gameState, 1, ghostNumber)

    def maximize(self, gameState, depth, ghostNumber):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        values = []
        actionToReturn = gameState.getLegalActions(0)[0]
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            values.append(self.minimize(successor, depth, 1, ghostNumber))
        if depth > 1:
            return max(values)
        else:
            for i in range(len(values)):
                if values[i] == max(values):
                    actionToReturn = gameState.getLegalActions(0)[i]
            return actionToReturn

    def minimize(self, gameState, depth, index, ghostNumber):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        values = []
        for action in gameState.getLegalActions(index):
            successor = gameState.generateSuccessor(index, action)
            if index != ghostNumber:
                values.append(self.minimize(successor, depth, index + 1, ghostNumber))
            else:
                if depth < self.depth:
                    values.append(self.maximize(successor, depth + 1, ghostNumber))
                else:
                    values.append(self.evaluationFunction(successor))
        return min(values)
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        ghostNumber = gameState.getNumAgents() - 1
        return self.maximize(gameState, 1, ghostNumber, -float('inf'), float('inf'))

    def maximize(self, gameState, depth, ghostNumber, alpha, beta):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        values = []
        actionToReturn = gameState.getLegalActions(0)[0]
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            values.append(self.minimize(successor, depth, 1, ghostNumber, alpha, beta))
            if max(values) > beta:
                return max(values)
            alpha = max(alpha, max(values))
        if depth > 1:
            return max(values)
        else:
            for i in range(len(values)):
                if values[i] == max(values):
                    actionToReturn = gameState.getLegalActions(0)[i]
            return actionToReturn

    def minimize(self, gameState, depth, index, ghostNumber, alpha, beta):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        values = []
        for action in gameState.getLegalActions(index):
            successor = gameState.generateSuccessor(index, action)
            if index != ghostNumber:
                values.append(self.minimize(successor, depth, index + 1, ghostNumber, alpha, beta))
            else:
                if depth < self.depth:
                    values.append(self.maximize(successor, depth + 1, ghostNumber, alpha, beta))
                else:
                    values.append(self.evaluationFunction(successor))
            if min(values) < alpha:
                return min(values)
            beta = min(beta, min(values))
        return min(values)

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        ghostNumber = gameState.getNumAgents() - 1
        return self.maximize(gameState, 1, ghostNumber)

    def maximize(self, gameState, depth, ghostNumber):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        values = []
        actionToReturn = gameState.getLegalActions(0)[0]
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            values.append(self.minimize(successor, depth, 1, ghostNumber))
        if depth > 1:
            return max(values)
        else:
            for i in range(len(values)):
                if values[i] == max(values):
                    actionToReturn = gameState.getLegalActions(0)[i]
            return actionToReturn

    def minimize(self, gameState, depth, index, ghostNumber):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        values = []
        for action in gameState.getLegalActions(index):
            successor = gameState.generateSuccessor(index, action)
            if index != ghostNumber:
                values.append(self.minimize(successor, depth, index + 1, ghostNumber))
            else:
                if depth < self.depth:
                    values.append(self.maximize(successor, depth + 1, ghostNumber))
                else:
                    values.append(self.evaluationFunction(successor))
        return sum(values) / len(values)
        util.raiseNotDefined()

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pacPos = currentGameState.getPacmanPosition()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    foodPos = currentGameState.getFood().asList()
    newFoodDistance = [manhattanDistance(xy, pacPos) for xy in foodPos]
    newGhostPos = [s.getPosition() for s in ghostStates]
    gameScore = currentGameState.getScore()
    foodCount = currentGameState.getNumFood()
    capCount = len(currentGameState.getCapsules())

    ghostDistance = []
    for i in range(len(ghostStates)):
        ghostDistance.append(manhattanDistance(newGhostPos[i], pacPos))

    if len(ghostDistance) > 0:
        for i in range(len(ghostStates)):
            if scaredTimes[i] > ghostDistance[i]:
                ghostDistance[i] = 200 - ghostDistance[i]
        minGhostDistance = min(ghostDistance)
    else:
        minGhostDistance = 0

    if len(newFoodDistance) > 0:
        minFoodDistance = min(newFoodDistance)
    else:
        minFoodDistance = 0

    return gameScore + minGhostDistance - 20 * capCount - 2 * minFoodDistance - 10 * foodCount


    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
