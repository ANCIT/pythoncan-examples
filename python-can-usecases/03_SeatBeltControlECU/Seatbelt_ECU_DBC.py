'''
Created on 30-Apr-2020

@author: bk
'''

import can
import cantools
import threading

bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=250000)
db = cantools.db.load_file('Basic_DBC.dbc')

brakeMsg = db.get_message_by_name('BrakeMsg')
accelerationMsg = db.get_message_by_name('AccelarationMsg')
seatbeltMsg = db.get_message_by_name('SeatbeltMsg')

def _lock_Seatbelt():
    data = seatbeltMsg.encode({'SeatbeltStatus':0,'SeatbeltLock':1,})
    message = can.Message(arbitration_id=seatbeltMsg.frame_id, data=data, is_extended_id=False)
    try:
        bus.send(message)
        print("SEATBELT LOCKED")
    except can.CanError:
        print("Message not sent")
        
def _unlock_Seatbelt():
    data = seatbeltMsg.encode({'SeatbeltStatus':0,'SeatbeltLock':0})
    message = can.Message(arbitration_id=seatbeltMsg.frame_id, data=data, is_extended_id=False)
    try:
        bus.send(message)
        print("SEATBELT UNLOCKED")
    except can.CanError:
        print("Message NOT sent")    

def on_Message():
    while True:
        message = bus.recv()
        msgData = db.decode_message(message.arbitration_id, message.data)
        if message.arbitration_id == accelerationMsg.frame_id:
            AcclrVal = (msgData['Acceleration'])
            if(AcclrVal == 0):
                _unlock_Seatbelt()
        if message.arbitration_id == brakeMsg.frame_id:
            _lock_Seatbelt()

if __name__ == '__main__':
    threading.Thread(on_Message()).start()