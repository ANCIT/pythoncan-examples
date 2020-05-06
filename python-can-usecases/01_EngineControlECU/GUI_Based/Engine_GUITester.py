import sys
import os
import can
import cantools
from threading import Thread
from pynput import keyboard

from PyQt5 import QtCore, QtGui, QtQml
from PyQt5.QtCore import QObject
from functools import partial

bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=250000)
db = cantools.db.load_file('Basic_DBC.dbc')

brakeMsg = db.get_message_by_name('BrakeMsg')
accelerationMsg = db.get_message_by_name('AccelarationMsg')
EngineMsg = db.get_message_by_name('VehicleMotion')

AcclrVal = 0
VhclSpeed = 0                
                  
def _accelerate(AcclrVal):
    data = accelerationMsg.encode({'Acceleration':AcclrVal})
    message = can.Message(arbitration_id=accelerationMsg.frame_id, data=data, is_extended_id=False)
    try:
        bus.send(message)
        print("\tAccelerated to: "+ str(AcclrVal))
    except can.CanError:
        print("Message not sent")
 
def _break():
    global AcclrVal
    data = brakeMsg.encode({'BrakeStatus':1})
    message = can.Message(arbitration_id=brakeMsg.frame_id, data=data, is_extended_id=False)
    try:
        bus.send(message)
        print("\tBreak Applied")
        AcclrVal = 0
    except can.CanError:
        print("Message not sent")


def on_press(key):
    try:
        if key.char == 'a': 
            _accelerate(10)
        if key.char == 'b':
            _break() 
    except AttributeError:
        print(" Unknown Key Event")

class on_Message(Thread):
    def __init__(self):
        Thread.__init__(self)
        
    def run(self):
        buffer = 0
        global VhclSpeed
        while True:
            message = bus.recv()
            msgData = db.decode_message(message.arbitration_id, message.data)
            if message.arbitration_id == EngineMsg.frame_id:
                EngineVelocity = (msgData['Velocity'])
                engineStat = bool(msgData['EngineRunning'])
                if(buffer != EngineVelocity):
                    print("Engine Speed Updated: " + str(EngineVelocity))
                    buffer = EngineVelocity
                    guiAppThread.updateSpeed(int(EngineVelocity))
                    guiAppThread.updateEngStat(engineStat)

        
class on_Key(Thread):
    def __init__(self):
        Thread.__init__(self)
        
    def run(self):
        keyboard.Listener(on_press=on_press).start()

class SpeedMeterManager(QtCore.QObject):
# Instance 
    speedChanged = QtCore.pyqtSignal(int)
    engStatChanged = QtCore.pyqtSignal(bool)
    brakeStatChanged = QtCore.pyqtSignal(bool)
    acclrtnChanged = QtCore.pyqtSignal(int)
        
    def __init__(self, parent=None):
            super(SpeedMeterManager, self).__init__(parent)
            self._speedVal = 0
            self._engStat = False
            self._brakeStat = False

    @QtCore.pyqtProperty(int, notify=speedChanged)
    def speedVal(self):
        return self._speedVal

    # Define the setter of the 'Speed' property.
    @speedVal.setter
    def speedVal(self, s):
        if self._speedVal != s:
            self._speedVal = s
            self.speedChanged.emit(s) 
        
    @QtCore.pyqtProperty(bool, notify=brakeStatChanged)
    def brakeStat(self):
        return self._brakeStat

    # Define the setter of the 'Brake' property.
    @brakeStat.setter
    def brakeStat(self, b):
        self._brakeStat = b
        self.brakeStatChanged.emit(b)
        
    @QtCore.pyqtProperty(bool, notify=engStatChanged)
    def engStat(self):
        return self._engStat

    # Define the setter of the 'Engine' property.
    @engStat.setter
    def engStat(self, c):
        self._engStat = c
        self.engStatChanged.emit(c)
    
    # Python type of the property is int.
    @QtCore.pyqtProperty(int, notify=acclrtnChanged)
    def acclVal(self):
        return self._acclVal

    # Define the setter of the 'Acceleration' property.
#     @acclVal.setter
#     def acclVal(self, a):
#         self._acclVal = a
#         self.acclrtnChanged.emit(a)

class gui_App (Thread):  
    def __init__(self):
        Thread.__init__(self)
        self.tempAccl = 0

    def launch(self):
        global VhclSpeed
        myApp = QtGui.QGuiApplication(sys.argv)
        myEngine = QtQml.QQmlApplicationEngine()
        self.manager = SpeedMeterManager()
        myEngine.rootContext().setContextProperty("smManager", self.manager)
        directory = os.path.dirname(os.path.abspath(__file__))
        myEngine.load(QtCore.QUrl.fromLocalFile(os.path.join(directory, 'speedMeter.qml')))
    
        if not myEngine.rootObjects():
            return -1
        self.dashB = myEngine.rootObjects()[0]
        timer = QtCore.QTimer(interval=500)
#         timer.timeout.connect(partial(self.updateSpeed, VhclSpeed))
        timer.timeout.connect(self.fetchBrake)
        timer.timeout.connect(self.fetchAccl)
        timer.start()
        return myApp.exec_()
    
    def updateSpeed(self, cGuageVal):
        self.manager.speedVal = cGuageVal
    
    def updateEngStat(self, engSt):
        self.manager.engStat = engSt
        
    def fetchBrake(self):
        brake = self.dashB.findChild(QObject, "brakBtn")
        brake_state = int(brake.property("checked"))
        if brake_state == True :
            _break()
        
    def fetchAccl(self):
        accl = self.dashB.findChild(QObject, "AcclSlider")
        C_acclVal = int(accl.property("value"))
        if C_acclVal != self.tempAccl:
            self.tempAccl = C_acclVal   
            _accelerate(C_acclVal)

if __name__ == '__main__':
    #Threads
    onKeyThread = on_Key()
    MsgRcvThread = on_Message()
    guiAppThread = gui_App()
    
    onKeyThread.start()
    guiAppThread.start()
    MsgRcvThread.start()
    # PrintInstructions
    print("Press below Keys to Test\n\t'a' to Accelerate\n\t'b' to Brake\n")
    #Launch GUI
    sys.exit(guiAppThread.launch())
    
    