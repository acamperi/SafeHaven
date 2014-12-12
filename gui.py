### Final Project Submission
### Students: Myles Novick & Ariel Camperi

import Tkinter as tk
import threading, time

class IconType(object):
	policePursuit = "policePursuit"
	policePatrol = "policePatrol"
	criminalSteal = "criminalSteal"
	criminalEscape = "criminalEscape"
	criminalGhost = "criminalGhost"
	mall = "mall"
	haven = "haven"
	station = "station"

class Icon(object):
	def __init__(self, posX, posY, iconType):
		if iconType == IconType.policePursuit:
			self.icon = IconType.policePursuit
			self.shape = "circle"
			self.color = "blue"
			self.posX = posX
			self.posY = posY
		elif iconType == IconType.policePatrol:
			self.icon = IconType.policePatrol
			self.shape = "circle"
			self.color = "green"
			self.posX = posX
			self.posY = posY
		elif iconType == IconType.criminalSteal:
			self.icon = IconType.criminalSteal
			self.shape = "circle"
			self.color = "orange"
			self.posX = posX
			self.posY = posY
		elif iconType == IconType.criminalEscape:
			self.icon = IconType.criminalEscape
			self.shape = "circle"
			self.color = "red"
			self.posX = posX
			self.posY = posY
		elif iconType == IconType.criminalGhost:
			self.icon = IconType.criminalGhost
			self.shape = "circle"
			self.color = "lavender"
			self.posX = posX
			self.posY = posY
		elif iconType == IconType.mall:
			self.icon = IconType.mall
			self.shape = "rectangle"
			self.color = "goldenrod"
			self.posX = posX
			self.posY = posY
		elif iconType == IconType.haven:
			self.icon = IconType.haven
			self.shape = "rectangle"
			self.color = "sienna"
			self.posX = posX
			self.posY = posY
		elif iconType == IconType.station:
			self.icon = IconType.station
			self.shape = "rectangle"
			self.color = "dark green"
			self.posX = posX
			self.posY = posY

class Board(object):
	def __init__(self, pixWidth=900, pixHeight=900):
		self.root = tk.Tk()
		self.canvasSize = (pixWidth, pixHeight)
		self.boardDimensions = (0, 0)
		self.boardIcons = []
		self.board = tk.Canvas(self.root, width=self.canvasSize[0], height=self.canvasSize[1])
		self.board.pack()
	def generate(self, width, height, icons=[]):
		pSize = (self.canvasSize[0] / width, self.canvasSize[1] / height)
		backgroundColors = ["floral white", "white smoke"]
		if (width, height) != self.boardDimensions:
			for a in xrange(width):
				for b in xrange(height):
					if a % 2:
						color = backgroundColors[0] if b % 2 else backgroundColors[1]
					else:
						color = backgroundColors[1] if b % 2 else backgroundColors[0]
					TL = (pSize[0] * a, pSize[1] * b)
					self.board.create_rectangle(TL[0], TL[1], pSize[0] + TL[0], pSize[1] + TL[1], fill=color)
			self.boardDimensions = (width, height)
		icons = filter(lambda i: isinstance(i, Icon) and i.posX in range(width) and i.posY in range(height), icons)
		iconFraction = .7
		iconSize = (pSize[0] * iconFraction, pSize[1] * iconFraction)
		for boardIcon in self.boardIcons:
			self.board.delete(boardIcon)
		self.boardIcons = []
		for icon in icons:
			TL = (pSize[0] * icon.posX + (pSize[0] - iconSize[0]) / 2., pSize[1] * icon.posY + (pSize[1] - iconSize[1]) / 2.)
			boardIcon = None
			if icon.shape == "rectangle":
				boardIcon = self.board.create_rectangle(TL[0], TL[1], iconSize[0] + TL[0], iconSize[1] + TL[1], fill=icon.color)
			elif icon.shape == "circle":
				boardIcon = self.board.create_oval(TL[0], TL[1], iconSize[0] + TL[0], iconSize[1] + TL[1], fill=icon.color)
			if boardIcon:
				self.boardIcons.append(boardIcon)
	def startDisplay(self):
		self.root.mainloop()
		for boardIcon in self.boardIcons:
			self.board.delete(boardIcon)
		self.boardIcons = []
	def stopDisplay(self):
		self.root.quit()

def demo():
	# demo code is below
	board = Board()
	board.generate(20, 20)
	def example():
		time.sleep(1)
		print "hello"
		board.generate(20, 20, [Icon(8, 3, IconType.policePursuit)])
		time.sleep(1)
		board.generate(20, 20, [Icon(1, 3, IconType.policePursuit)])
	threading.Thread(target=example).start()
	board.startDisplay()
