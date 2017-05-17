import com
from time import sleep, time
import scipy.interpolate
import scipy.fftpack
import scipy.signal
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *

class VFC():

	def __init__(self, ui):
		self.points = []
		self.lines = []

		self.testDuration = 300000
		
		self.VFCx = []
		self.VFCy = []

		self.ui = ui

		self.block = False

	def calcVFC(self):

		N = 3000000
		x = np.linspace(self.VFCx[0], self.VFCx[-1], N)
		y = np.interp(x, self.VFCx, self.VFCy)

		file = open("save/thomas.ibi",'w',encoding="utf-8")

		for i in range(len(self.VFCx)):
			file.write(str(self.VFCx[i]) + ',' + str(self.VFCy[i]) + '\n')
		file.close()

		yDetrend = scipy.signal.detrend(y)
		yf = scipy.fftpack.fft(yDetrend)[range(N//2)]
		xf = scipy.fftpack.fftfreq(y.size, x[1] - x[0])[range(N//2)]

		useless, LF, HF = 0,0,0

		for i in xf:
			if (i <= 0.04):
				useless += 1
			elif (0.04 <= i <= 0.15):
				LF += 1
			elif (0.15 <= i <= 0.4):
				HF += 1

		yfPow = [abs(cell * cell) for cell in yf]

		areaLF = scipy.integrate.simps(yfPow[useless:LF])
		areaHF = scipy.integrate.simps(yfPow[LF:HF])

		VFC = areaLF / areaHF

		print(areaLF, areaHF, VFC)

		fig, ax = plt.subplots()
		ax.plot(xf, yf)
		ax.set_xlim(0,0.4)

		fig2, ax2 = plt.subplots()
		plt.scatter(self.VFCx, self.VFCy, s=4, color='red')
		ax2.plot(x, y)
		plt.show(block=False)

		self.ui.resultVFC('VFC : ' + str(round(VFC, 3)))

	def newPoint(self, x, y):

		if (int(x) < self.testDuration):
			self.points.append([int(x)/1000, 60/int(y.strip())])
			self.VFCx.append(int(x)/1000)
			self.VFCy.append(round(60/int(y.strip()), 5))

			if (len(self.points) > 1):

				x1 = (((self.points[-1][0] * 1000) / self.testDuration)) * 1000
				y1 = 190 - (round(self.points[-1][1],5) * 200) / 1.5 + 5
				x2 = (((self.points[-2][0] * 1000) / self.testDuration)) * 1000
				y2 = 190 - (round(self.points[-2][1],5) * 200) / 1.5 + 5

				self.lines.append(self.ui.createLineVFC(x1, y1, x2, y2))

		else:
			if (not self.block):
				self.calcVFC()
				self.block = True
