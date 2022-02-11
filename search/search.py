# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

class Node:
    def __init__(self, state, pred, action, priority=0):
        self.state = state
        self.pred = pred
        self.action = action
        self.priority = priority
    def __repr__(self):
        return "State: {0}, Action: {1}".format(self.state, self.action)

T = 0

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    closed = list()
    path = util.Stack()

    def dfs(state):
        global T
        closed.append(state)
        if problem.isGoalState(state):
            T = 1
            return
        adj = problem.getSuccessors(state)
        for node in list(reversed(adj)):
            if node[0] not in closed:
                dfs(node[0])
                if T == 1:
                    path.push(node[1])
                    return

    dfs(problem.getStartState())
    global T
    T = 0
    return list(reversed(path.list))
    util.raiseNotDefined()



def breadthFirstSearch(problem):
    "Search the shallowest nodes in the search tree first."
    "*** YOUR CODE HERE ***"

    def bfs():
        closed = list()
        path = {}
        fringe = util.Queue()
        fringe.push(problem.getStartState())
        while not fringe.isEmpty():
            state = fringe.pop()
            closed.append(state)
            if problem.isGoalState(state):
                return path, state
            adj = problem.getSuccessors(state)
            for node in adj:
                if node[0] not in fringe.list and node[0] not in closed:
                    path[node[0]] = [state, node[1]]
                    fringe.push(node[0])

    path, last = bfs()
    p = []
    while last in path:
        p.append(path[last][1])
        last = path[last][0]
    return list(reversed(p))

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    def ucs():
        closed = list()
        path = {}
        fringe = util.PriorityQueue()
        fringe1 = {}
        fringe.push(problem.getStartState(), 0)
        fringe1[problem.getStartState()] = (0, 0, problem.getStartState())
        while not fringe.isEmpty():
            state = fringe.pop()
            temp = fringe1.pop(state)
            closed.append(state)
            if problem.isGoalState(state):
                return path, state
            adj = problem.getSuccessors(state)
            for node in adj:
                if node[0] not in fringe1.keys() and node[0] not in closed:
                    path[node[0]] = [state, node[1]]
                    fringe1[node[0]] = (temp[0] + node[2], len(fringe.heap), node[0])
                    fringe.push(node[0], temp[0] + node[2])
                if node[0] in fringe1.keys() and temp[0] + node[2] < fringe1[node[0]][0]:
                    path[node[0]] = [state, node[1]]


    path, last = ucs()
    p = []
    while last in path:
        p.append(path[last][1])
        last = path[last][0]
    return list(reversed(p))

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    def a_star():
        closed = list()
        path = {}
        fringe = util.PriorityQueue()
        fringe1 = {}
        fringe.push(problem.getStartState(), heuristic(problem.getStartState(), problem))
        print(fringe.heap)
        fringe1[problem.getStartState()] = (0, 0, problem.getStartState())
        while not fringe.isEmpty():
            state = fringe.pop()
            temp = fringe1.pop(state)
            closed.append(state)
            if problem.isGoalState(state):
                return path, state
            adj = problem.getSuccessors(state)
            for node in adj:
                if node[0] not in fringe1.keys() and node[0] not in closed:
                    path[node[0]] = [state, node[1]]
                    fringe1[node[0]] = (temp[0] + node[2], len(fringe.heap), node[0])
                    fringe.push(node[0], temp[0] + node[2] + heuristic(node[0], problem))
                if node[0] in fringe1.keys() and temp[0] + node[2] < fringe1[node[0]][0]:
                    path[node[0]] = [state, node[1]]
                    fringe.update(node[0], temp[0] + node[2] + heuristic(node[0], problem))


    path, last = a_star()
    p = []
    while last in path:
        p.append(path[last][1])
        last = path[last][0]
    return list(reversed(p))



    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
