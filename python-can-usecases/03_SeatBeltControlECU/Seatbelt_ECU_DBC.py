'''
Created on 15-Apr-2020

@author: bk
'''
import can
import cantools

bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=250000)
db = cantools.db.load_file('Basic_DBC.dbc')

seatbeltMsg = db.get_message_by_name('SeatbeltMsg')
seatbeltReqMsg = db.get_message_by_name('SeatbeltReqMsg')

while True:
    message = bus.recv()
    msgData = db.decode_message(message.arbitration_id, message.data)
    print(seatbeltReqMsg.frame_id)
    print(message.arbitration_id)
    if message.arbitration_id == seatbeltReqMsg.frame_id:
        print("Req Recieved")
        seatbeltReq = (msgData['SeatbeltReq'])
        if (seatbeltReq == 'UnLockReq'):
            # Send Seatbelt Release Message
            data = seatbeltMsg.encode({'SeatbeltStatus':0})
            message = can.Message(arbitration_id=seatbeltMsg.frame_id, data=data, is_extended_id=False)
            try:
                bus.send(message)
                print('Seat Belt Un-Locked')
            except can.CanError:
                print("Message NOT sent")
        
        if (seatbeltReq == 'LockReq'):
            # Send Seatbelt Lock Message
            data = seatbeltMsg.encode({'SeatbeltStatus':1})
            message = can.Message(arbitration_id=seatbeltMsg.frame_id, data=data, is_extended_id=False)
            try:
                bus.send(message)
                print('Seat Belt Locked')
            except can.CanError:
                print("Message NOT sent")

