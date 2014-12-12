### Final Project Submission
### Students: Myles Novick & Ariel Camperi

from util import *

class CriminalState(object):
    """ Configuration values to describe a criminal agent's state. """
    STEAL = 'steal'
    ESCAPE = 'escape'
    SAFE = 'safe'
    CAUGHT = 'caught'

class CriminalAgent(Agent):
    """
    This class encapsulates state data about a criminal agent, but also logic about
    what action to take given a simulation state, and about how to execute an
    action and properly update state data. Initialized with a position.
    """
    def __init__(self, pos):
        super(CriminalAgent, self).__init__(pos)
        self.state = CriminalState.STEAL
        self.justCommittedCrime = False
    def copy(self):
        """
        Creates a copy of the criminal agent, and copies over relevant properties.
        """
        copy = CriminalAgent((self.x, self.y))
        copy.state = self.state
        copy.justCommittedCrime = self.justCommittedCrime
        return copy
    def isActive(self):
        """ Criminals remain active while they are in steal or escape modes. """
        return self.state not in [CriminalState.SAFE, CriminalState.CAUGHT]
    def getAction(self, simulationState):
        """
        Given a simulation state, generates a list of legal actions, and uses the
        evaluation function to determine the optimal successor state (depth 1).
        """
        if self.state == CriminalState.SAFE or self.state == CriminalState.CAUGHT:
            return Directions.STOP
        i = simulationState.criminalAgents.index(self)
        legalActions = simulationState.getLegalActionsForAgent(self)
        legalSuccessors = [simulationState.generateSuccessorForCriminalAction(action, i) for action in legalActions]
        evals = [self.evaluationFunction(successor, successor.criminalAgents[i]) for successor in legalSuccessors]
        return legalActions[evals.index(max(evals))]
    def evaluationFunction(self, simulationState, agent):
        """
        While stealing, the criminal will favor proximity to malls, and want to stay
        away from nearby detected police agents. While escaping, the criminal will
        try to get to haven as quickly as possible, again while avoiding nearby 
        detected police agents.
        """
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
        """
        Calls super implementation to update position, then updates status based
        on surrounding conditions (e.g. collisions with police agents).
        """
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
