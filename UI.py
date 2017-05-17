from tkinter import *
from com import *

class UI(Tk):

	def __init__(self, ports):
		Tk.__init__(self)
		self.geometry("1400x850")
		self.resizable(0,0)
		self.title('Contrôle ECG')
		self.ecgC = None
		self.ecg = None
		self.vfc = None
		self.var = StringVar()
		self.var.trace('w', self.UIChangePort)
		self.drop = OptionMenu(self, self.var, ports)
		self.drop.place(x=20,y=20)

		self.etat = Label(self, text="Déconnecté", font=("Segoe UI", 15))
		self.etat.place(x=120, y=16)

		Label(self, text="Console", font=("Segoe UI", 13)).place(x=1100, y=20)

		self.console = Text(width=40,height=48, bd=0, font=("Consolas", 10))
		self.console.bind("<Key>", lambda e: "break")
		self.console.place(x=1100, y=50)

		self.e = Entry(self, bd=0, font=("Consolas", 10), width=40, state=DISABLED)
		self.e.place(x=1100, y=780)

		self.e.bind("<Return>", self.UICommand)

		self.debug = IntVar()
		self.c = Checkbutton(self, text='Débug', variable=self.debug, borderwidth=1)
		self.c.place(x=1100, y=800)

		self.sound = IntVar()
		self.c2 = Checkbutton(self, text='Sound', variable=self.sound, borderwidth=1)
		self.c2.place(x=1300, y=800)

	def connected(self):
		self.e.config(state='normal')

		self.delayT = Label(self, text="Délai (ms)", font=("Segoe UI", 12))
		self.delayT.place(x=50, y=300)

		self.delay = Label(self, text="0", font=("Segoe UI", 12))
		self.delay.place(x=130, y=300)

		self.BPM = Label(self, text='??', font=("Segoe UI", 20))
		self.BPM.place(x=1000, y=300)

		self.ecgC = Canvas(self, width=1000, height=200, bg="light green")
		self.ecgC.place(x=50, y=100)

		self.btn1 = Button(self, width=20, text='ECG', command=lambda:com.sendECG(self))
		self.btn1.place(x=325, y=380)

		self.btn2 = Button(self, width=20, text='VFC', command=lambda:com.sendVFC(self))
		self.btn2.place(x=625, y=380)

	def UICommand(self, event):
		command = self.e.get()
		self.e.delete(0, END)
		send(self, command)

	def log(self, text, dir):
		self.console.tag_config('ECG', foreground='red')
		self.console.tag_config('PC', foreground='blue')
		self.console.tag_config('INFO', background='pink', foreground='white')
		self.console.see('end')
		if (dir == 'ECG' or dir == 'INFO'):
			self.console.insert(END, text + '\n', dir)
		else:
			self.console.insert(END, text, dir)

	def changeState(self, text):
		self.etat.config(text=text)

	def UIChangePort(self, *args):
		port = self.var.get()
		setPort(self, port)

	def createLine(self, x1, y1, x2, y2):
		return self.ecgC.create_line(x1, y1, x2, y2, fill="white", width=2)

	def createLineVFC(self, x1, y1, x2, y2):
		return self.vfcC.create_line(x1, y1, x2, y2, fill="white")

	def dispTime(self, delay):
		self.delay.config(text=delay)

	def dispBPM(self, BPM):
		self.BPM.config(text=BPM)

	def ecgSpread(self, ecg = None):
		if (ecg == None):
			return self.ecg
		else:
			self.ecg = ecg

	def startVFC(self, vfc):
		self.vfcC = Canvas(self, width=1000, height=200, bg="light blue")
		self.vfcC.place(x=50, y=500)
		self.vfc = vfc

	def vfcSpread(self):
		return self.vfc

	def resultVFC(self, result):
		self.result = Label(self, text=result, font=("Segoe UI", 20))
		self.result.place(x=500, y=750)