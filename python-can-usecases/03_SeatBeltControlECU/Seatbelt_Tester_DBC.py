'''
Created on 15-Apr-2020

@author: bk
'''

import can
from pynput import keyboard
import threading
import cantools

bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=250000)
db = cantools.db.load_file('Basic_DBC.dbc')

seatbeltMsg = db.get_message_by_name('SeatbeltMsg')
seatbeltReqMsg = db.get_message_by_name('SeatbeltReqMsg')

def on_press(key):
    try:
        if key.char == 'a': # for unlock
            data = seatbeltReqMsg.encode({'SeatbeltReq':1})
            message = can.Message(arbitration_id=seatbeltReqMsg.frame_id, data=data, is_extended_id=False)
            try:
                bus.send(message)
                print("Message sent: \tTrigger Seatbelt Lock")
            except can.CanError:
                print("Message NOT sent")
        
        if key.char == 'b': # for lock
            data = seatbeltReqMsg.encode({'SeatbeltReq':0})
            message = can.Message(arbitration_id=seatbeltReqMsg.frame_id, data=data, is_extended_id=False)
            try:
                bus.send(message)
                print("Message sent: \tTrigger Seatbelt Un-Lock")
            except can.CanError:
                print("Message NOT sent")
                
    except AttributeError:
        pass
 
def on_Key():
#     with keyboard.Listener(on_press=on_press) as listener:
#         listener.join()
    keyboard.Listener(on_press=on_press).start()

def on_Message():
    while True:
        message = bus.recv()
        msgData = db.decode_message(message.arbitration_id, message.data)
        if message.arbitration_id == seatbeltMsg.frame_id:
            seatbeltStatus = (msgData['SeatbeltStatus'])
            if (seatbeltStatus == 'NotWorn'):
                    #if Seatbelt is not Locked
                    print("\tResponse: Seatbelt Un-Locked")
            if (seatbeltStatus == 'Worn'):
                    #if Seatbelt is Locked
                    print("\tResponse: Seatbelt Locked")

if __name__ == '__main__':
    print("Press keys 'a' or 'b' to Test\n")
    on_Key()
    threading.Thread(on_Message()).start()