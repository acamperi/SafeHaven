### Final Project Submission
### Students: Myles Novick & Ariel Camperi

class Directions(object):
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

class Agent(object):
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
    def getPos(self):
        return (self.x, self.y)
    def getAction(self, simulationState):
        return Directions.STOP
    def executeAction(self, action):
        self.x, self.y = Directions.successor(self.getPos(), action)
