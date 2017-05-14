import com
from time import sleep, time
from tkinter import *

class ECG():

	def __init__(self, ui):
		self.points = []
		self.lines = []
		self.BPM = [0] * 6

		self.ui = ui

	def start(self):
		self.ui.connected()

	def newPoint(self, x, y):
		self.points.append([int(x), int(y.strip())])

		if (len(self.points) == 1):
			self.startTime = time()

		delay = abs(int(x) - (time() - self.startTime) * 1000)

		self.ui.dispTime(str(int(delay)))

		if (len(self.points) > 1):

			x1 = ((self.points[-1][0] * 1000) / 5000) % 1000
			y1 = 190 - (self.points[-1][1] * 190) / 1023 + 5
			x2 = ((self.points[-2][0] * 1000) / 5000) % 1000
			y2 = 190 - (self.points[-2][1] * 190) / 1023 + 5

			if (x2 - x1 >= 0):
				self.ui.ecgC.delete('all')
			else:
				self.lines.append(self.ui.createLine(x1, y1, x2, y2))

	def BPMCalc(self, t):
		self.BPM = [t] + self.BPM[:-1]

		if (self.BPM[5] != self.BPM[4]):
			self.ui.dispBPM(str(int(300000 / (self.BPM[0] - self.BPM[5]))))