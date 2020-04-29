'''
Created on 15-Apr-2020

@author: bk
'''
import can
bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=250000)

seatbeltMsgID = 0x101
seatbeltReqMsgID = 0x107

while True:
    message = bus.recv()
    msgData = message.data
    if message.arbitration_id == seatbeltReqMsgID: 
        
        if (msgData[0] == 0x01):
            msg = can.Message(arbitration_id=seatbeltMsgID,data=[1, 0],is_extended_id=False)
            try:
                bus.send(msg)
                print('Seat Belt Locked')
            except can.CanError:
                print("Message NOT sent")
        
        if (msgData[0] == 0x00):
            msg = can.Message(arbitration_id=seatbeltMsgID,data=[0, 0],is_extended_id=False)
            try:
                bus.send(msg)
                print('Seat Belt Locked')
            except can.CanError:
                print("Message NOT sent")

