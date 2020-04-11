'''
Created on 24-Mar-2020

@author: ancit
'''
import can
bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=250000)
msg = can.Message(arbitration_id=0xc0ffee,data=[0, 25, 0, 1, 3, 1, 4, 1],is_extended_id=False)
try:
    bus.send_periodic(msg,0.2)
    print("Message sent on {}".format(bus.channel_info))
except can.CanError:
    print("Message NOT sent")

