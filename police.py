### Final Project Submission
### Students: Myles Novick & Ariel Camperi

from util import *

class PoliceState(object):
    PATROL = 'patrol'
    PURSUIT = 'pursuit'

class PoliceAgent(Agent):
    def __init__(self, pos):
        super(PoliceAgent, self).__init__(pos)
        self.state = PoliceState.PATROL
        self.pursuedCriminal = None
        self.pursuedCriminalPosGuess = None
    def copy(self):
        copy = PoliceAgent(self.getPos())
        copy.state = self.state
        return copy
    def doPreProcessing(self, simulationState):
        pass
    def getAction(self, simulationState):
        return Directions.STOP
    def executeAction(self, action, simulationState):
        super(PoliceAgent, self).executeAction(action)
        if self.state == PoliceState.PURSUIT and self.getPos() == simulationState.criminalAgents[self.pursuedCriminal].getPos():
            self.state = PoliceState.PATROL

class DispatcherAgent(object):
    @staticmethod
    def getPoliceActions(simulationState):
        for p in simulationState.policeAgents:
            p.doPreProcessing(simulationState)
        return [p.getAction(simulationState) for p in simulationState.policeAgents]
