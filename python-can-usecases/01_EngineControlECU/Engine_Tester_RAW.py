import can
import threading
from pynput import keyboard

bus = can.interface.Bus(bustype='socketcan',channel='vcan0',bitrate=250000)

brakeMsgID = 0x105
accelerationMsgID = 0x106
EngineMsgID = 0x104

AcclrVal = 0

def _accelerate():
    global AcclrVal
    AcclrVal = AcclrVal+2
    
    message = can.Message(arbitration_id=accelerationMsgID,data=[AcclrVal, 0],is_extended_id=False)
    try:
        bus.send(message)
        print("\tAccelerated to: "+ str(AcclrVal))
    except can.CanError:
        print("Message not sent")

def _decelerate():
    global AcclrVal
    AcclrVal = AcclrVal-2
    
    message = can.Message(arbitration_id=accelerationMsgID,data=[AcclrVal, 0],is_extended_id=False)
    try:
        bus.send(message)
        print("\tAccelerated to: "+ str(AcclrVal))
    except can.CanError:
        print("Message not sent")
 
def _break():
    global AcclrVal
    message = can.Message(arbitration_id=brakeMsgID, data=[0,0], is_extended_id=False)
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
        msgData = message.data
        if message.arbitration_id == EngineMsgID:   
            EngineVelocity = msgData[1]
            if(buffer != EngineVelocity):
                print("Engine Speed Updated: " + str(EngineVelocity))
                buffer = EngineVelocity
        
def on_Key():
    keyboard.Listener(on_press=on_press).start()

if __name__ == '__main__':
    print("Press below Keys to Test\n\t'a' to Accelerate\n\t'd' to Decelerate\n\t'b' to Brake\n")
    on_Key()
    threading.Thread(on_Message()).start()