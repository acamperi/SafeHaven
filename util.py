### Final Project Submission
### Students: Myles Novick & Ariel Camperi

class Directions(object):
    NORTH = 'North'
    SOUTH = 'South'
    EAST = 'East'
    WEST = 'West'
    STOP = 'Stop'

class Station(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Mall(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Haven(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Agent(object):
    def getAction(self, state):
        return Directions.STOP
