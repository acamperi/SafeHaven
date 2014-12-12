### Final Project Submission
### Students: Myles Novick & Ariel Camperi

import math

""" Configuration values """
POLICE_TURNS_PER_CRIMINALS = 1
CRIMINAL_SIGHT_RADIUS = 1
POLICE_SIGHT_RADIUS = 5
MAX_POLICE_PER_CRIMINAL = 5
MIN_POLICE_DISTANCE_TO_PURSUE = 10

class Directions(object):
    """
    Useful constants for grid actions, and utility method for calculating action effects.
    """
    NORTH = 'North'
    SOUTH = 'South'
    EAST = 'East'
    WEST = 'West'
    STOP = 'Stop'

    @staticmethod
    def successor(pos, action):
        if action == Directions.NORTH:
            return (pos[0], pos[1] - 1)
        if action == Directions.SOUTH:
            return (pos[0], pos[1] + 1)
        if action == Directions.EAST:
            return (pos[0] + 1, pos[1])
        if action == Directions.WEST:
            return (pos[0] - 1, pos[1])
        return pos

# class Station(object):
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y

# class Mall(object):
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y

# class Haven(object):
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y

def manhattanDistance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def euclideanDistance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

class Agent(object):
    """
    Superclass for PoliceAgent and CriminalAgent. Shared functionality like
    initialization, position helpers, and other method stubs.
    """
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
    def getPos(self):
        return (self.x, self.y)
    def setPos(self, pos):
        self.x, self.y = pos
    def getAction(self, simulationState):
        return Directions.STOP
    def executeAction(self, action):
        self.x, self.y = Directions.successor(self.getPos(), action)
