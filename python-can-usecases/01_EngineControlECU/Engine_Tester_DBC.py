import can
import cantools
import threading
from pynput import keyboard

bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=250000)
db = cantools.db.load_file('Basic_DBC.dbc')

brakeMsg = db.get_message_by_name('BrakeMsg')
accelerationMsg = db.get_message_by_name('AccelarationMsg')
EngineMsg = db.get_message_by_name('VehicleMotion')

AcclrVal = 0

def _accelerate():
    global AcclrVal
    AcclrVal = AcclrVal+10
    
    data = accelerationMsg.encode({'Acceleration':AcclrVal})
    message = can.Message(arbitration_id=accelerationMsg.frame_id, data=data, is_extended_id=False)
    try:
        bus.send(message)
        print("\tAccelerated to: "+ str(AcclrVal))
    except can.CanError:
        print("Message not sent")

def _decelerate():
    global AcclrVal
    AcclrVal = AcclrVal-10
    
    data = accelerationMsg.encode({'Acceleration':AcclrVal})
    message = can.Message(arbitration_id=accelerationMsg.frame_id, data=data, is_extended_id=False)
    try:
        bus.send(message)
        print("\tDecelerated to "+ str(AcclrVal))
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
            _accelerate()
        if key.char == 'd':
            _decelerate()
        if key.char == 'b':
            _break() 
    except AttributeError:
        print(" Unknown Key Event")
        
def on_Message():
    buffer = 0
    while True:
        message = bus.recv()
        msgData = db.decode_message(message.arbitration_id, message.data)
        if message.arbitration_id == EngineMsg.frame_id:
            EngineVelocity = (msgData['Velocity'])
            if(buffer != EngineVelocity):
                print("Engine Speed Updated: " + str(EngineVelocity))
                buffer = EngineVelocity
        
def on_Key():
    keyboard.Listener(on_press=on_press).start()

if __name__ == '__main__':
    print("Press below Keys to Test\n\t'a' to Accelerate\n\t'd' to Decelerate\n\t'b' to Brake\n")
    on_Key()
    threading.Thread(on_Message()).start()
    