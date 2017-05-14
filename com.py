import sys
import serial
from ecg import *
from time import sleep

BAUDRATE = 2000000
s = None

def listPorts():

	ports = ['COM' + str(i + 1) for i in range (256)]
	portsOK = []

	for port in ports:
		try:
			s = serial.Serial(port)
			s.close()
			portsOK.append(port)
		except (OSError, serial.SerialException):
			pass

	return portsOK

def setPort(ui, newPort):
	port = newPort[2:6]
	connect(ui, port)

def connect(ui, port):
	global s
	s = serial.Serial(port, BAUDRATE, timeout=0.00001)
	ui.changeState('Connexion à ' + port)
	ui.update()
	sleep(0.2)
	if (s.is_open):
		ui.changeState('Connecté à ' + port)
		ui.log(' Connecté (Baudrate ' + str(BAUDRATE) + ')', 'INFO')
		ecg = ECG(ui)
		ecg.start()
		ui.ecgSpread(ecg)
		ui.after(2000, start, ui)
	else:
		ui.changeState(' Echec de la connexion')

def start(ui):
	send(ui,'START')

def close():
	global s
	s.close()

def send(ui, text):
	global s
	s.write(text.encode())
	ui.log('>> ' + text, 'ECG')

def isConnected():
	global s
	if (s != None):
		if (s.is_open):
			return True
		else:
			return False
	else:
		return False

def read(ui):
	global s
	try:
		msg = s.readline()
		if (len(msg) != 0):
			if (msg.decode()[:5] == 'START' or msg.decode()[:4] == 'STOP') and not ui.debug.get():
				ui.log('<< ' + msg.decode(), 'PC')
			if ui.debug.get():
				ui.log('<< ' + msg.decode(), 'PC')
			return msg.decode()
		else:
			return None
	except (OSError, serial.SerialException):
		close()
		ui.changeState(' Connexion perdue')
		ui.log(' Déconnecté', 'INFO')