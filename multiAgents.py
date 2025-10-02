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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
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

    def evaluationFunction(self, currentGameState: GameState, action):
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
        #score = successorGameState.getScore()
        score = 0

        #so that pacmans dont get stop in some corner
        if action == 'Stop':
            score -= 100

        #distance to the closest food
        foodList = newFood.asList()
        minDistance = 100000
        score += -len(foodList) * 100
        for food in foodList:
            distance = manhattanDistance(food, newPos)
            if distance < minDistance:
                minDistance = distance
        #making pacman to go to the closest food
        score += -minDistance
        if foodList == []:
            score += 10000 + minDistance

        #if neraest ghost is close to pacman, pacman should avoid it
        for ghost in newGhostStates:
            ghostPos = ghost.getPosition()
            distance = manhattanDistance(ghostPos, newPos)
            if distance < 2:
                score -= 100000

        return score

def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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
        def maxLayer(state, depth):
            #if the game is over or the depth is 0, return the score and the action
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state), None
            
            bestScore = float("-inf")

            #for each action, get the score and the action
            for action in state.getLegalActions(0):
                tmp = minLayer(state.generateSuccessor(0, action), depth, 1)
                if tmp > bestScore:
                    bestScore = tmp
                    bestAction = action
            return (bestScore, bestAction)
        def minLayer(state, depth, agentIndex):
            #if the game is over or the depth is 0, return the score
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
            
            bestScore = float("inf")

            #for each action, get the score
            for action in state.getLegalActions(agentIndex):
                if agentIndex == state.getNumAgents() - 1:
                    bestScore = min(bestScore, maxLayer(state.generateSuccessor(agentIndex, action), depth - 1)[0])
                else:
                    bestScore = min(bestScore, minLayer(state.generateSuccessor(agentIndex, action), depth, agentIndex + 1))
            return bestScore
        
        #return the action
        return maxLayer(gameState, self.depth)[1]
              

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maxLayer(state, depth, alpha = float("-inf"), beta = float("inf")):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state), "STOP"
            bestScore = float("-inf")
            #different from minimax, we need to pass alpha and beta to the next layer
            alphaToPass = alpha
            for action in state.getLegalActions(0):
                #condition to prune
                if bestScore > beta:
                    return (bestScore, action)
                alphaToPass = max(alphaToPass, bestScore)
                tmp = minLayer(state.generateSuccessor(0, action), depth, 1, alphaToPass, beta)
                if tmp > bestScore:
                    bestScore = tmp
                    bestAction = action
            return (bestScore, bestAction)
        def minLayer(state, depth, agentIndex, alpha = float("-inf"), beta = float("inf")):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
            bestScore = float("inf")
            betaToPass = beta
            for action in state.getLegalActions(agentIndex):
                #condition to prune
                if bestScore < alpha:
                    return bestScore
                betaToPass = min(betaToPass, bestScore)
                if agentIndex == state.getNumAgents() - 1:
                    bestScore = min(bestScore, maxLayer(state.generateSuccessor(agentIndex, action), depth - 1, alpha, betaToPass)[0])
                else:
                    bestScore = min(bestScore, minLayer(state.generateSuccessor(agentIndex, action), depth, agentIndex + 1, alpha, betaToPass))
            return bestScore
        return maxLayer(gameState, self.depth)[1]
        #util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def maxLayer(state, depth):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state), "STOP"
            bestScore = -100000000
            for action in state.getLegalActions(0):
                tmp = minLayer(state.generateSuccessor(0, action), depth, 1)
                if tmp > bestScore:
                    bestScore = tmp
                    bestAction = action
            return (bestScore, bestAction)
        def minLayer(state, depth, agentIndex):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
            bestScore = 0
            for action in state.getLegalActions(agentIndex):
                #only difference from minimax is that we need to sum the scores
                if agentIndex == state.getNumAgents() - 1:
                    bestScore += maxLayer(state.generateSuccessor(agentIndex, action), depth - 1)[0]
                else:
                    bestScore += minLayer(state.generateSuccessor(agentIndex, action), depth, agentIndex + 1)
            return bestScore / len(state.getLegalActions(agentIndex))
        return maxLayer(gameState, self.depth)[1]
       # util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    score = scoreEvaluationFunction(currentGameState)
    current_pos = currentGameState.getPacmanPosition()
    ghostStates = currentGameState.getGhostStates() 
    food = currentGameState.getFood()
    nearestFood = 0

    if len(food.asList()) != 0:
        nearestFood = min([manhattanDistance(current_pos, ff) for ff in food.asList()])

    nearestGhost = -4
    ghost_distances = [manhattanDistance(current_pos, ghostState.getPosition()) for ghostState in ghostStates if ghostState.scaredTimer == 0]
    nearest_scared_ghost = 0
    scared_ghost_distance = [manhattanDistance(current_pos, ghostState.getPosition()) for ghostState in ghostStates if ghostState.scaredTimer > 0]

    if currentGameState.isWin():  
        return float(99999)

    if currentGameState.isLose(): 
        return float(-99999)

    if len(ghost_distances) > 0:
        nearestGhost = min(ghost_distances)


    
    if (len(scared_ghost_distance) > 0): 
        nearest_scared_ghost = min(scared_ghost_distance)
    finish = 1
    if len(food.asList()) == 1:
        finish = 100
    return score + 1 / nearestFood - (1 / nearestGhost)  - 3*nearest_scared_ghost - 40*len(currentGameState.getCapsules()) - len(food.asList())
    
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
