### Final Project Submission
### Students: Myles Novick & Ariel Camperi

import random, sys, argparse, copy
from math import *
from util import *
from police import *
from criminal import *
from gui import *

class SimulationParameters(object):
    def __init__(self):
        self.N = 0
        self.S = 0
        self.P = 0
        self.M = 0
        self.H = 0
        self.C = 0
        self.S_pos = []
        self.P_pos = []
        self.M_pos = []
        self.H_pos = []
        self.C_pos = []
    def generatePositions(self, N, S, P, M, H, C):
        self.N = N
        self.S = S
        self.P = P
        self.M = M
        self.H = H
        self.C = C
        claimedPositions = []
        for pair in [(self.S, self.S_pos), (self.M, self.M_pos), (self.H, self.H_pos), (self.P, self.P_pos), (self.C, self.C_pos)]:
            for i in xrange(pair[0]):
                pos = (random.randrange(0, self.N), random.randrange(0, self.N))
                while pos in claimedPositions:
                    pos = (random.randrange(0, self.N), random.randrange(0, self.N))
                pair[1].append(pos)
                claimedPositions.append(pos)
    def readFromFile(self, filename):
        def posListFromComponents(components):
            return [(int(pos[0]), int(pos[1])) for pos in map(lambda p: p.split("|"), components)]
        with open(filename) as infile:
            for line in infile.readlines():
                components = line.strip().split(" ")
                if components[0] == "N:":
                    self.N = int(components[1])
                elif components[0] == "S:":
                    self.S = len(components[1:])
                    self.S_pos = posListFromComponents(components[1:])
                elif components[0] == "M:":
                    self.M = len(components[1:])
                    self.M_pos = posListFromComponents(components[1:])
                elif components[0] == "H:":
                    self.H = len(components[1:])
                    self.H_pos = posListFromComponents(components[1:])
                elif components[0] == "P:":
                    self.P = len(components[1:])
                    self.P_pos = posListFromComponents(components[1:])
                elif components[0] == "C:":
                    self.C = len(components[1:])
                    self.C_pos = posListFromComponents(components[1:])

class SimulationState(object):
    def __init__(self, params=None):
        if params is not None:
            self.N = params.N
            # self.stations = [Station(pos[0], pos[1]) for pos in params.S_pos]
            # self.malls = [Mall(pos[0], pos[1]) for pos in params.M_pos]
            # self.havens = [Haven(pos[0], pos[1]) for pos in params.H_pos]
            self.stations = params.S_pos
            self.malls = params.M_pos
            self.havens = params.H_pos
            self.policeAgents = [PoliceAgent(pos) for pos in params.P_pos]
            self.criminalAgents = [CriminalAgent(pos) for pos in params.C_pos]
        else:
            self.N = 0
            self.stations = []
            self.malls = []
            self.havens = []
            self.policeAgents = []
            self.criminalAgents = []
    def copy(self, copyAgents=True):
        state = SimulationState()
        state.N = self.N
        # state.stations = [Station(s.x, s.y) for s in self.stations]
        # state.malls = [Mall(m.x, m.y) for m in self.malls]
        # state.havens = [Haven(h.x, h.y) for h in self.havens]
        state.stations = copy.copy(self.stations)
        state.malls = copy.copy(self.malls)
        state.havens = copy.copy(self.havens)
        if copyAgents:
            state.policeAgents = [p.copy() for p in self.policeAgents]
            state.criminalAgents = [c.copy() for c in self.criminalAgents]
        else:
            state.policeAgents = copy.copy(self.policeAgents)
            state.criminalAgents = copy.copy(self.criminalAgents)
        return state
    def getLegalActionsForAgent(self, agent):
        legalActions = [Directions.STOP]
        if agent.x > 0:
            legalActions.append(Directions.WEST)
        if agent.y > 0:
            legalActions.append(Directions.NORTH)
        if agent.x < self.N - 1:
            legalActions.append(Directions.EAST)
        if agent.y < self.N - 1:
            legalActions.append(Directions.SOUTH)
        return legalActions
    def generateSuccessorForPoliceAction(self, action, i):
        successor = self.copy(False)
        successor.policeAgents[i] = successor.policeAgents[i].copy()
        successor.policeAgents[i].executeAction(action, successor)
        return successor
    def generateSuccessorForCriminalAction(self, action, i):
        successor = self.copy(False)
        successor.criminalAgents[i] = successor.criminalAgents[i].copy()
        successor.criminalAgents[i].executeAction(action, successor)
        return successor
    def generateSuccessor(self, policeActions, criminalActions):
        successor = self.copy()
        for j in xrange(len(successor.criminalAgents)):
            successor.criminalAgents[j].executeAction(criminalActions[j], successor)
        for i in xrange(len(successor.policeAgents)):
            successor.policeAgents[i].executeAction(policeActions[i], successor)
        for k in xrange(len(successor.criminalAgents)):
            successor.criminalAgents[k].executeAction(Directions.STOP, successor)
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
        return "%d stations, %d malls, %d havens, %d police, %d criminals" % \
        (len(self.stations), len(self.malls), len(self.havens), len(self.policeAgents), len(self.criminalAgents))

class Simulation(object):
    def __init__(self, params, board, sleepTime):
        self.state = SimulationState(params)
        self.board = board
        self.sleepTime = sleepTime
        print self.state
    def run(self):
        while not self.state.isFinal():
            print "STEP"
            for i in xrange(POLICE_TURNS_PER_CRIMINALS - 1):
                policeActions = DispatcherAgent.getPoliceActions(self.state)
                self.state = self.state.generateSuccessor(policeActions, [Directions.STOP for c in self.state.criminalAgents])
                display(self.state, self.board)
                time.sleep(self.sleepTime)
            policeActions = DispatcherAgent.getPoliceActions(self.state)
            criminalActions = [c.getAction(self.state) for c in self.state.criminalAgents]
            self.state = self.state.generateSuccessor(policeActions, criminalActions)
            display(self.state, self.board)
            time.sleep(self.sleepTime)
        print "%d criminals were caught, %d got away" % (self.state.getNumCaughtCriminals(), self.state.getNumSafeCriminals())
        self.board.stopDisplay()

def display(state, board):
    def iconTypeForPoliceAgent(policeAgent):
        if policeAgent.state == PoliceState.PURSUIT:
            return IconType.policePursuit
        return IconType.policePatrol
    def iconTypeForCriminalAgent(criminalAgent):
        if criminalAgent.state == CriminalState.ESCAPE:
            return IconType.criminalEscape
        return IconType.criminalSteal
    # stationIcons = [Icon(s.x, s.y, IconType.station) for s in state.stations]
    # mallIcons = [Icon(m.x, m.y, IconType.mall) for m in state.malls]
    # havenIcons = [Icon(h.x, h.y, IconType.haven) for h in state.havens]
    stationIcons = [Icon(s[0], s[1], IconType.station) for s in state.stations]
    mallIcons = [Icon(m[0], m[1], IconType.mall) for m in state.malls]
    havenIcons = [Icon(h[0], h[1], IconType.haven) for h in state.havens]
    policeIcons = [Icon(p.x, p.y, iconTypeForPoliceAgent(p)) for p in state.policeAgents]
    # criminalIcons = [Icon(pos[0], pos[1], IconType.criminalGhost) for pos in set([police.pursuedCriminalPosGuess for police in state.policeAgents if police.pursuedCriminalPosGuess and police.state == PoliceState.PURSUIT])]
    criminalIcons = [Icon(c.x, c.y, iconTypeForCriminalAgent(c)) for c in state.criminalAgents if c.state != CriminalState.CAUGHT]
    icons = stationIcons + mallIcons + havenIcons + policeIcons + criminalIcons
    board.generate(state.N, state.N, icons)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", dest="infile", default=None)
    parser.add_argument("-t", dest="sleepTime", type=float, default=0.3)
    args = parser.parse_args()
    params = SimulationParameters()
    if args.infile is None:
        params.generatePositions(30, 1, 5, 1, 2, 2)
    else:
        params.readFromFile(args.infile)
    board = Board()
    sim = Simulation(params, board, args.sleepTime)
    board.generate(sim.state.N, sim.state.N)
    threading.Thread(target=sim.run).start()
    board.startDisplay()

if __name__ == '__main__':
    main()
