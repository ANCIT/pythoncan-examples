'''
Created on 30-Apr-2020

@author: bk
'''

import can
import threading

bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=250000)

seatbeltMsgID = 0x101
brakeMsgID = 0x105
accelerationMsgID = 0x106

def _lock_Seatbelt():
    message = can.Message(arbitration_id=seatbeltMsgID, data=[3,0,0,0], is_extended_id=False)
    #Seatbelt Worn and Lock
    try:
        bus.send(message)
        print("SEATBELT LOCKED")
    except can.CanError:
        print("Message not sent")
        
def _unlock_Seatbelt():
    message = can.Message(arbitration_id=seatbeltMsgID, data=[1,0,0,0], is_extended_id=False)
    #Seatbelt Worn but unLock
    try:
        bus.send(message)
        print("SEATBELT UN-LOCKED")
    except can.CanError:
        print("Message not sent")    

def on_Message():
    while True:
        message = bus.recv()
        msgData = message.data
        if message.arbitration_id == accelerationMsgID: 
            if((msgData[0] == 0) and (msgData[1] == 0)):    #Check the Value in 2bytes == 0
                _unlock_Seatbelt()
                
        if message.arbitration_id == brakeMsgID:
            _lock_Seatbelt()

if __name__ == '__main__':
    threading.Thread(on_Message()).start()