from com import *
from UI import *
from time import *
from ecg import *
from VFC import *
import atexit

s = None

ports = listPorts()
ui = UI(ports)

high = False

atexit.register(close)

def main():
    global high

    if (isConnected()):
        msg = read(ui)
        ecg = ui.ecgSpread()
        vfc = ui.vfcSpread()

        if (msg != None):
            if (msg[:1] == 'D'):
                array = msg.split(';')

                if (len(array) == 3):
                    if (array[2] != ''):
                        ecg.newPoint(array[1], array[2])

                        if (int(array[2]) >= 400 and not high):
                            high = True
                            ecg.BPMCalc(int(array[1]))
                        elif (int(array[2]) <= 400 and high):
                            high = False

            elif (msg[:1] == 'V'):
                array = msg.split(';')
                if (len(array) == 3):
                    if (array[2] != ''):
                        vfc.newPoint(array[1], array[2])

            elif (msg[:9] == 'START VFC'):
                ui.startVFC(VFC(ui))
    ui.after(1, main)

main()
ui.mainloop()