### Final Project Submission
### Students: Myles Novick & Ariel Camperi

import random, sys, argparse
from math import *
from util import *
from police import *
from criminal import *
from gui import *

class SimulationParameters(object):
    def __init__(self, N, S, P, M, H, C):
        self.N = N
        self.S = S
        self.P = P
        self.M = M
        self.H = H
        self.C = C
        self.S_pos = []
        self.P_pos = []
        self.P_patrolAreas = []
        self.M_pos = []
        self.H_pos = []
        self.C_pos = []
        self.generatePositions()

    def generatePositions(self):
        for s in xrange(self.S):
            self.S_pos.append((random.randrange(0, self.N), random.randrange(0, self.N)))
        for m in xrange(self.M):
            self.M_pos.append((random.randrange(0, self.N), random.randrange(0, self.N)))
        for h in xrange(self.H):
            self.H_pos.append((random.randrange(0, self.N), random.randrange(0, self.N)))
        for c in xrange(self.C):
            self.C_pos.append((random.randrange(0, self.N), random.randrange(0, self.N)))
        rootP = int(sqrt(self.P))
        patrolSize = int(float(self.N) / float(rootP))
        halfPatrolSize = int(patrolSize / 2)
        x = halfPatrolSize
        y = halfPatrolSize
        for p in xrange(self.P):
            self.P_pos.append((x, y))
            x += patrolSize
            if x >= self.N:
                x = halfPatrolSize
            y += patrolSize
            self.P_patrolAreas.append((x - halfPatrolSize, y - halfPatrolSize, patrolSize, patrolSize))

    @staticmethod
    def readFromFile(filename):
        pass

class SimulationState(object):
    def __init__(self, params=None):
        if params is not None:
            self.N = params.N
            self.stations = [Station(pos[0], pos[1]) for pos in params.S_pos]
            self.malls = [Mall(pos[0], pos[1]) for pos in params.M_pos]
            self.havens = [Haven(pos[0], pos[1]) for pos in params.H_pos]
            self.policeAgents = [PoliceAgent(params.P_pos[i], params.P_patrolAreas[i]) for i in xrange(params.P)]
            self.criminalAgents = [CriminalAgent(pos) for pos in params.C_pos]
        else:
            self.N = 0
            self.stations = []
            self.malls = []
            self.havens = []
            self.policeAgents = []
            self.criminalAgents = []
    def copy(self):
        copy = SimulationState()
        copy.N = self.N
        copy.stations = [Station(s.x, s.y) for s in self.stations]
        copy.malls = [Mall(m.x, m.y) for m in self.malls]
        copy.havens = [Haven(h.x, h.y) for h in self.havens]
        copy.policeAgents = [p.copy() for p in self.policeAgents]
        copy.criminalAgents = [c.copy() for c in self.criminalAgents]
        return copy
    def generateSuccessor(self, policeActions, criminalActions):
        successor = self.copy()
        for i in xrange(len(successor.policeAgents)):
            successor.policeAgents[i].executeAction(policeActions[i])
        for j in xrange(len(successor.criminalAgents)):
            successor.criminalAgents[j].executeAction(criminalActions[j])
        return successor
    def isFinal(self):
        for c in self.criminalAgents:
            if c.isActive():
                return False
        return True
    def getNumSafeCriminals(self):
        return len(filter(lambda c: c.state == CriminalState.SAFE, self.criminalAgents))
    def getNumCaughtCriminals(self):
        return len(filter(lambda c: c.state == CriminalState.CAUGHT, self.criminalAgents))
    def __str__(self):
        return "%d stations, %d malls, %d havens, %d police, %d criminals" % (len(self.stations), len(self.malls), len(self.havens), len(self.policeAgents), len(self.criminalAgents))

class Simulation(object):
    def __init__(self, params, board):
        self.state = SimulationState(params)
        self.board = board
        print self.state
    def run(self):
        global sleepTime
        while not self.state.isFinal():
            print "STEP"
            policeActions = DispatcherAgent.getPoliceActions(self.state)
            criminalActions = [c.getAction(self.state) for c in self.state.criminalAgents]
            print policeActions
            print criminalActions
            self.state = self.state.generateSuccessor(policeActions, criminalActions)
            display(self.state, self.board)
            time.sleep(sleepTime)
        print "%d criminals were caught, %d got away" % (self.state.getNumCaughtCriminals(), self.state.getNumSafeCriminals())

def display(state, board):
    def iconTypeForPoliceAgent(policeAgent):
        if policeAgent.state == PoliceState.PURSUIT:
            return IconType.policePursuit
        return IconType.policePatrol
    def iconTypeForCriminalAgent(criminalAgent):
        if criminalAgent.state == CriminalState.ESCAPE:
            return IconType.criminalEscape
        return IconType.criminalSteal
    stationIcons = [Icon(s.x, s.y, IconType.station) for s in state.stations]
    mallIcons = [Icon(m.x, m.y, IconType.mall) for m in state.malls]
    havenIcons = [Icon(h.x, h.y, IconType.haven) for h in state.havens]
    policeIcons = [Icon(p.x, p.y, iconTypeForPoliceAgent(p)) for p in state.policeAgents]
    criminalIcons = [Icon(c.x, c.y, iconTypeForCriminalAgent(c)) for c in state.criminalAgents]
    icons = stationIcons + mallIcons + havenIcons + policeIcons + criminalIcons
    board.generate(state.N, state.N, icons)

sleepTime = 0.5

def main(argv):
    global sleepTime
    if len(argv):
        sleepTime = float(argv[0])
    params = SimulationParameters(100, 3, 9, 2, 3, 5)
    board = Board()
    sim = Simulation(params, board)
    board.generate(sim.state.N, sim.state.N)
    threading.Thread(target=sim.run).start()
    board.startDisplay()

if __name__ == '__main__':
    main(sys.argv[1:])
