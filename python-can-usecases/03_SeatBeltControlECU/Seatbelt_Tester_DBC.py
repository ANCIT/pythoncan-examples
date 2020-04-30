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
brakeMsg = db.get_message_by_name('BrakeMsg')
accelerationMsg = db.get_message_by_name('AccelarationMsg')

def on_press(key):
    try:
        if key.char == 'a': # for Acceleration
            data = accelerationMsg.encode({'Acceleration':0})
            message = can.Message(arbitration_id=accelerationMsg.frame_id, data=data, is_extended_id=False)
            try:
                bus.send(message)
                print("Message sent: \tVehicle Stopped Moving")
            except can.CanError:
                print("Message NOT sent")
        
        if key.char == 'b': # for lock
            data = brakeMsg.encode({'BrakeStatus':1})
            message = can.Message(arbitration_id=brakeMsg.frame_id, data=data, is_extended_id=False)
            try:
                bus.send(message)
                print("Message sent: \tSudden Break Applaid")
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
            seatbeltStatus = (msgData['SeatbeltLock'])
            if (seatbeltStatus == 'UnLock'):
                    #if Seatbelt is not Locked
                    print("\tResponse: Seatbelt Un-Locked")
            if (seatbeltStatus == 'Lock'):
                    #if Seatbelt is Locked
                    print("\tResponse: Seatbelt Locked")

if __name__ == '__main__':
    print("Press keys 'a' or 'b' to Test\n")
    on_Key()
    threading.Thread(on_Message()).start()