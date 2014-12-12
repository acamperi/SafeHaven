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
        super(CriminalAgent, self).__init__(pos)
        self.state = CriminalState.STEAL
    def copy(self):
        copy = CriminalAgent((self.x, self.y))
        copy.state = self.state
        return copy
    def isActive(self):
        return self.state not in [CriminalState.SAFE, CriminalState.CAUGHT]
    def getAction(self, simulationState):
        return Directions.STOP
    def executeAction(self, action, simulationState):
        super(CriminalAgent, self).executeAction(action)
        currPos = self.getPos()
        if self.state == CriminalState.STEAL and currPos in simulationState.malls:
            self.state = CriminalState.ESCAPE
        if self.state == CriminalState.ESCAPE:
            if currPos in simulationState.havens:
                self.state = CriminalState.SAFE
            else:
                for policeAgent in simulationState.policeAgents:
                    if currPos == policeAgent.getPos():
                        self.state = CriminalState.CAUGHT
                        break
