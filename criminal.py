### Final Project Submission
### Students: Myles Novick & Ariel Camperi

from util import *

class CriminalState(object):
    STEAL = 'steal'
    ESCAPE = 'escape'
    SAFE = 'safe'
    CAUGHT = 'caught'

class CriminalAgent(Agent):
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.state = CriminalState.STEAL
    def copy(self):
        copy = CriminalAgent((self.x, self.y))
        copy.state = self.state
        return copy
    def isActive(self):
        return self.state not in [CriminalState.SAFE, CriminalState.CAUGHT]
    def getAction(self, simulationState):
        return Directions.STOP
