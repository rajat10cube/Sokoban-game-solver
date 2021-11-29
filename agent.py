#########################################
#                                       #
#                                       #
#  ==  SOKOBAN STUDENT AGENT CODE  ==   #
#                                       #
#      Written by: Rajat Raghuwanshi    #
#                                       #
#                                       #
#########################################


# SOLVER CLASSES WHERE AGENT CODES GO
from helper import *
import random
import math


# Base class of agent (DO NOT TOUCH!)
class Agent:
    def getSolution(self, state, maxIterations):
        return []       # set of actions


#####       EXAMPLE AGENTS      #####

# Do Nothing Agent code - the laziest of the agents
class DoNothingAgent(Agent):
    def getSolution(self, state, maxIterations):
        if maxIterations == -1:     # RIP your machine if you remove this block
            return []

        #make idle action set
        nothActionSet = []
        for i in range(20):
            nothActionSet.append({"x":0,"y":0})

        return nothActionSet

# Random Agent code - completes random actions
class RandomAgent(Agent):
    def getSolution(self, state, maxIterations):

        #make random action set
        randActionSet = []
        for i in range(20):
            randActionSet.append(random.choice(directions))

        return randActionSet


#####    ASSIGNMENT 1 AGENTS    #####
# BFS Agent code
class BFSAgent(Agent):
    def getSolution(self, state, maxIterations=-1):
        intializeDeadlocks(state)
        iterations = 0
        bestNode = None
        queue = [Node(state.clone(), None, None)]   #state, parent, action
        visited = []

        while (iterations < maxIterations or maxIterations <= 0) and len(queue) > 0:
            iterations += 1

            # YOUR CODE HERE
            if iterations == 1:                 # Initializing bestNode variable to 1st node only once
                bestNode = queue[0]
            currNode = queue.pop(0)             # currNode = first node of list (FIFO Queue implementation)
            if bestNode.getHeuristic() == currNode.getHeuristic():
                if bestNode.getCost() > currNode.getCost():
                    bestNode = currNode         # if heuristic is same, comparing cost and setting bestNode
            elif bestNode.getHeuristic() > currNode.getHeuristic():
                bestNode = currNode             # if heuristic is not same, setting bestNode
            if bestNode.checkWin():
                break                           # if win state reached, break out of while loop to reach return
            if currNode.getHash() in visited:
                continue                        # if currNode already in visited, don't do anything
            visited.append(currNode.getHash())  # adding getHash function of currNode to visited
            children = currNode.getChildren()
            for child in children:
                if child.getHash() not in visited:  # checking child in visited without increasing complexity
                    queue.append(child)             # if child was not in visited, we add the child to queue

        return bestNode.getActions()


# DFS Agent Code
class DFSAgent(Agent):
    def getSolution(self, state, maxIterations=-1):
        intializeDeadlocks(state)
        iterations = 0
        bestNode = None
        queue = [Node(state.clone(), None, None)]
        visited = []
        #expand the tree until the iterations runs out or a solution sequence is found
        while (iterations < maxIterations or maxIterations <= 0) and len(queue) > 0:
            iterations += 1

            # YOUR CODE HERE
            if iterations == 1:                 # Initializing bestNode variable only once
                bestNode = queue[0]
            currNode = queue.pop()              # currNode = last node of list (LIFO Stack implementation)
            if bestNode.getHeuristic() == currNode.getHeuristic():
                if bestNode.getCost() > currNode.getCost():
                    bestNode = currNode
            elif bestNode.getHeuristic() > currNode.getHeuristic():
                bestNode = currNode
            if bestNode.checkWin():
                break
            if currNode.getHash() in visited:
                continue
            visited.append(currNode.getHash())
            children = currNode.getChildren()
            for child in children:
                if child.getHash() not in visited:
                    queue.append(child)

        return bestNode.getActions()


# AStar Agent Code
class AStarAgent(Agent):
    def getSolution(self, state, maxIterations=-1):
        #setup
        intializeDeadlocks(state)
        iterations = 0
        bestNode = None

        #initialize priority queue
        queue = PriorityQueue()
        queue.put(Node(state.clone(), None, None))
        visited = []
        while (iterations < maxIterations or maxIterations <= 0) and queue.qsize() > 0:
            iterations += 1

            ## YOUR CODE HERE ##
            if iterations == 1:
                bestNode = Node(state.clone(), None, None)  # Initialization of bestNode only once
            currNode = queue.get()              # currNode = first node of Priority Queue
            if bestNode.getHeuristic() == currNode.getHeuristic():
                if bestNode.getCost() > currNode.getCost():
                    bestNode = currNode
            elif bestNode.getHeuristic() > currNode.getHeuristic():
                bestNode = currNode
            if bestNode.checkWin():
                break
            if currNode.getHash() in visited:
                continue
            visited.append(currNode.getHash())
            for child in currNode.getChildren():
                cost = child.getHeuristic() + child.getCost()
                if child.getHash() not in visited:
                    queue.put(child, cost)

        return currNode.getActions()
