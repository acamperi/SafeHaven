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
        self.justCommittedCrime = False
    def copy(self):
        copy = CriminalAgent((self.x, self.y))
        copy.state = self.state
        copy.justCommittedCrime = self.justCommittedCrime
        return copy
    def isActive(self):
        return self.state not in [CriminalState.SAFE, CriminalState.CAUGHT]
    def getAction(self, simulationState):
        if self.state == CriminalState.SAFE or self.state == CriminalState.CAUGHT:
            return Directions.STOP
        i = simulationState.criminalAgents.index(self)
        legalActions = simulationState.getLegalActionsForAgent(self)
        legalSuccessors = [simulationState.generateSuccessorForCriminalAction(action, i) for action in legalActions]
        evals = [self.evaluationFunction(successor, successor.criminalAgents[i]) for successor in legalSuccessors]
        return legalActions[evals.index(max(evals))]
    def evaluationFunction(self, simulationState, agent):
        currPos = agent.getPos()
        currState = agent.state
        if currState == CriminalState.STEAL:
            closestMallDistance = 1. / (float(min([euclideanDistance(currPos, mallPos) for mallPos in simulationState.malls])) + 0.00001)
            detectedPoliceAgents = [police for police in simulationState.policeAgents if euclideanDistance(currPos, police.getPos()) <= CRIMINAL_SIGHT_RADIUS]
            return closestMallDistance - float(len(detectedPoliceAgents))
        elif currState == CriminalState.ESCAPE:
            closestHavenDistance = 1. / (float(min([euclideanDistance(currPos, havenPos) for havenPos in simulationState.havens])) + 0.00001)
            detectedPoliceAgents = [police for police in simulationState.policeAgents if euclideanDistance(currPos, police.getPos()) <= CRIMINAL_SIGHT_RADIUS]
            return 1. + closestHavenDistance - float(len(detectedPoliceAgents))
        elif currState == CriminalState.CAUGHT:
            return -999999
        elif currState == CriminalState.SAFE:
            return 999999
    def executeAction(self, action, simulationState):
        super(CriminalAgent, self).executeAction(action)
        currPos = self.getPos()
        if self.state == CriminalState.STEAL and currPos in simulationState.malls:
            self.state = CriminalState.ESCAPE
            self.justCommittedCrime = True
        elif self.state == CriminalState.ESCAPE:
            self.justCommittedCrime = False
            if currPos in simulationState.havens:
                self.state = CriminalState.SAFE
            else:
                for policeAgent in simulationState.policeAgents:
                    if currPos == policeAgent.getPos():
                        self.state = CriminalState.CAUGHT
                        break
