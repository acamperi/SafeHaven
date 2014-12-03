### Final Project Submission
### Students: Myles Novick & Ariel Camperi

from util import *

class PoliceState(object):
    PATROL = 'patrol'
    PURSUIT = 'pursuit'

class PoliceAgent(Agent):
    def __init__(self, pos, patrolArea):
        self.x = pos[0]
        self.y = pos[1]
        self.patrolArea = patrolArea
        self.state = PoliceState.PATROL
    def copy(self):
        copy = PoliceAgent((self.x, self.y), self.patrolArea)
        copy.state = self.state
        return copy
    def doPreProcessing(self, simulationState):
        pass
    def getAction(self, simulationState):
        return Directions.STOP

class DispatcherAgent(object):
    @staticmethod
    def getPoliceActions(simulationState):
        for p in simulationState.policeAgents:
            p.doPreProcessing(simulationState)
        return [p.getAction(simulationState) for p in simulationState.policeAgents]
