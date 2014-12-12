### Final Project Submission
### Students: Myles Novick & Ariel Camperi

import random
from util import *
from criminal import CriminalState

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
        copy.pursuedCriminal = self.pursuedCriminal
        copy.pursuedCriminalPosGuess = self.pursuedCriminalPosGuess
        return copy
    def checkForCriminalSightings(self, simulationState):
        currPos = self.getPos()
        return [i for i in xrange(len(simulationState.criminalAgents)) if euclideanDistance(currPos, simulationState.criminalAgents[i].getPos()) <= POLICE_SIGHT_RADIUS and simulationState.criminalAgents[i].state == CriminalState.ESCAPE]
    def alphabeta(self, simulationState, agents, i, depth, alpha, beta):
        i %= len(agents)
        if depth <= 0 or simulationState.isFinal():
            return self.pursuitEvaluationFunction(simulationState, agents[self.index])
        elif isinstance(agents[i], PoliceAgent):
            for legalAction in simulationState.getLegalActionsForAgent(agents[i]):
                successor = simulationState.generateSuccessorForPoliceAction(legalAction, i)
                agents = successor.policeAgents + [successor.criminalAgents[self.pursuedCriminal]]
                alpha = max(alpha, self.alphabeta(successor, agents, i + 1, depth - 1, alpha, beta))
                if alpha >= beta:
                    return alpha
            return alpha
        else:
            criminalPosGuess = None
            for legalAction in simulationState.getLegalActionsForAgent(agents[i]):
                successor = simulationState.generateSuccessorForCriminalAction(legalAction, self.pursuedCriminal)
                agents = successor.policeAgents + [successor.criminalAgents[self.pursuedCriminal]]
                beta = min(beta, self.alphabeta(successor, agents, i + 1, depth - 1, alpha, beta))
                if alpha >= beta:
                    return beta
            return beta
    def patrolEvaluationFunction(self, simulationState, agent):
        distancesToOtherPolice = [euclideanDistance(agent.getPos(), police.getPos()) for police in simulationState.policeAgents if police != agent]
        if not distancesToOtherPolice:
            return 1. / (float(euclideanDistance(agent.getPos(), (simulationState.N / 2, simulationState.N / 2))) + 0.00001)
        wallDistances = []
        currPos = agent.getPos()
        wallDistances.append(euclideanDistance(currPos, (0, agent.y)))
        wallDistances.append(euclideanDistance(currPos, (simulationState.N - 1, agent.y)))
        wallDistances.append(euclideanDistance(currPos, (agent.x, simulationState.N - 1)))
        wallDistances.append(euclideanDistance(currPos, (agent.x, 0)))
        return float(sum(distancesToOtherPolice)) / ((float(len(distancesToOtherPolice)) + 0.00001)) + min(wallDistances) * float(random.randrange(3))
    def pursuitEvaluationFunction(self, simulationState, agent):
        if agent.state == PoliceState.PATROL:
            if simulationState.criminalAgents[agent.pursuedCriminal].state == CriminalState.SAFE:
                return -999999
            else:
                return 999999
        distanceToCriminal = 1. / (float(euclideanDistance(agent.getPos(), agent.pursuedCriminalPosGuess)) + 0.00001)
        criminalDistanceToClosestHaven = 1. / (float(min([euclideanDistance(agent.pursuedCriminalPosGuess, havenPos) for havenPos in simulationState.havens])) + 0.00001)
        return 2. * distanceToCriminal + criminalDistanceToClosestHaven
    def criminalEvaluationFunction(self, simulationState, agent):
        if agent.state == CriminalState.CAUGHT:
            return -999999
        elif agent.state == CriminalState.SAFE:
            return 999999
        else:
            closestHavenDistance = 1. / (float(min([euclideanDistance(agent.getPos(), havenPos) for havenPos in simulationState.havens])) + 0.00001)
            return closestHavenDistance
    def getCriminalGuessPos(self, simulationState):
        criminal = simulationState.criminalAgents[self.pursuedCriminal]
        legalActions = simulationState.getLegalActionsForAgent(criminal)
        legalSuccessors = [simulationState.generateSuccessorForCriminalAction(action, self.pursuedCriminal) for action in legalActions]
        evals = [self.criminalEvaluationFunction(successor, successor.criminalAgents[self.pursuedCriminal]) for successor in legalSuccessors]
        successorChoices = [legalSuccessors[evals.index(max(evals))], random.choice(legalSuccessors)]
        return random.choice(successorChoices).criminalAgents[self.pursuedCriminal].getPos()
    def getAction(self, simulationState):
        i = simulationState.policeAgents.index(self)
        legalActions = simulationState.getLegalActionsForAgent(self)
        if self.state == PoliceState.PATROL:
            legalSuccessors = [simulationState.generateSuccessorForPoliceAction(action, i) for action in legalActions]
            evals = [self.patrolEvaluationFunction(successor, successor.policeAgents[i]) for successor in legalSuccessors]
            return legalActions[evals.index(max(evals))]
        else:
            stateGuess = simulationState.generateSuccessorForCriminalAction(Directions.STOP, self.pursuedCriminal)
            stateGuess.criminalAgents[self.pursuedCriminal].setPos(self.pursuedCriminalPosGuess)
            legalSuccessors = [stateGuess.generateSuccessorForPoliceAction(action, i) for action in legalActions]
            agents = stateGuess.policeAgents + [stateGuess.criminalAgents[self.pursuedCriminal]]
            self.index = i
            evals = [self.alphabeta(successor, agents, i + 1, 2 * len(agents) - 1, float("-inf"), float("inf")) for successor in legalSuccessors]
            self.pursuedCriminalPosGuess = self.getCriminalGuessPos(simulationState)
            return legalActions[evals.index(max(evals))]
    def executeAction(self, action, simulationState):
        super(PoliceAgent, self).executeAction(action)
        if self.state == PoliceState.PURSUIT and (self.getPos() == simulationState.criminalAgents[self.pursuedCriminal].getPos() or (self.getPos() == self.pursuedCriminalPosGuess)):
            self.state = PoliceState.PATROL
    def __str__(self):
        return "Pos = " + str(self.getPos()) + " ; " + str(self.state) + " ; C = " + str(self.pursuedCriminal) + " ; C_pos = " + str(self.pursuedCriminalPosGuess)

class DispatcherAgent(object):
    @staticmethod
    def getPoliceActions(simulationState):
        sightedCriminals = set([i for i in xrange(len(simulationState.criminalAgents)) if simulationState.criminalAgents[i].justCommittedCrime])
        for police in simulationState.policeAgents:
            sightedCriminals |= set(police.checkForCriminalSightings(simulationState))

        availablePoliceAgents = []
        policeAgentsInPursuit = []
        for police in simulationState.policeAgents:
            if police.pursuedCriminal in sightedCriminals:
                police.state = PoliceState.PATROL
            if police.state == PoliceState.PATROL:
                availablePoliceAgents.append(police)
            else:
                policeAgentsInPursuit.append(police)

        numPolicePerSightedCriminal = {(c, simulationState.criminalAgents[c].getPos()) : 0 for c in sightedCriminals}
        for police in policeAgentsInPursuit:
            key = (police.pursuedCriminal, police.pursuedCriminalPosGuess)
            numPolicePerSightedCriminal[key] = 0 if key not in numPolicePerSightedCriminal else numPolicePerSightedCriminal[key] + 1
        criminalsToPursueOrderedKeys = sorted(numPolicePerSightedCriminal, key=lambda x: numPolicePerSightedCriminal[x])
        while availablePoliceAgents:
            assignmentHappened = False
            for criminal, criminalPos in criminalsToPursueOrderedKeys:
                if numPolicePerSightedCriminal[(criminal, criminalPos)] >= MAX_POLICE_PER_CRIMINAL:
                    continue
                closestPoliceAgent = min(availablePoliceAgents, key=lambda p: euclideanDistance(p.getPos(), criminalPos))
                if numPolicePerSightedCriminal[(criminal, criminalPos)] > 0 and euclideanDistance(closestPoliceAgent.getPos(), criminalPos) > MIN_POLICE_DISTANCE_TO_PURSUE:
                    continue
                closestPoliceAgent.state = PoliceState.PURSUIT
                closestPoliceAgent.pursuedCriminal = criminal
                closestPoliceAgent.pursuedCriminalPosGuess = criminalPos
                availablePoliceAgents.remove(closestPoliceAgent)
                policeAgentsInPursuit.append(closestPoliceAgent)
                numPolicePerSightedCriminal[(criminal, criminalPos)] += 1
                assignmentHappened = True
                if not availablePoliceAgents:
                    break
            if not assignmentHappened:
                break

        return [p.getAction(simulationState) for p in simulationState.policeAgents]
