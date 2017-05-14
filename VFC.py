import com
from time import sleep, time
from tkinter import *

class VFC():

	def __init__(self, ui):
		self.points = []
		self.lines = []
		
		self.VFCx = []
		self.VFCy = []

		self.ui = ui

	def newPoint(self, x, y):
		self.points.append([int(x), int(y.strip())])
		self.VFCx.append(int(x))
		self.VFCy.append(int(y.strip()))

		if (len(self.points) > 1):

			x1 = ((self.points[-1][0] * 1000) / 600000)
			y1 = 190 - (self.points[-1][1] * 190) / 300 + 5
			x2 = ((self.points[-2][0] * 1000) / 600000)
			y2 = 190 - (self.points[-2][1] * 190) / 300 + 5

			self.lines.append(self.ui.createLineVFC(x1, y1, x2, y2))

		print(self.VFCx, self.VFCy)