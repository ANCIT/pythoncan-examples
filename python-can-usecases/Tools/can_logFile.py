"""
The Script will Log Can BUS and Display in Console 
 
Configure the Bus and Filter under bus_Config Class

Filter - Can add the multiple coma separated filters.
    Fx: 100:7FC  : Will allow only can_id 100 to 103
        120:FF0  : Will allow only can_id containing 12X.
        140:7BF  : Will allow only can_id 120
    
    <can_id>:<can_mask> (matches when<received_can_id> & mask == can_id & mask)
    <can_id>~<can_mask> (matches when<received_can_id> & mask != can_id & mask)
        
Press Esc Key to Save the Logfile with configured file name and terminate program 
    - Can mention the directory along with name
    - incase of only name, the file will save in the same directory of script
    - file extension also can be choose (.log, .txt, etc)
-------------------
Created by Manzoor
"""

from __future__ import absolute_import, print_function

import socket
from datetime import datetime
from pynput import keyboard

from can import Bus, Logger
keep_going = True

class bus_Cofing ():
    def __init__(self):
        self.channel = 'vcan0'
        self.interface = 'socketcan'
        self.bitrate = 250000
        self.filter = ['120:FF0', '140:7BF']
        self.log_file = 'logSample.txt'
        
def logCan():       
    results = bus_Cofing()

    can_filters = []
    if len(results.filter) > 0:
        print('Adding filter are:')
        for filt in results.filter:
            if ':' in filt:
                _ = filt.split(":")
                can_id = int(_[0], base=16)
                can_mask = int(_[1], base=16)
                print('Can ID: ', hex(can_id), 'mask: ', hex(can_mask))
                
            elif "~" in filt:
                can_id, can_mask = filt.split("~")
                can_id = int(can_id, base=16) | 0x20000000    # CAN_INV_FILTER
                can_mask = int(can_mask, base=16) & socket.CAN_ERR_FLAG
                print('Can ID: ', can_id, 'mask: ', can_mask)
            can_filters.append({"can_id": can_id, "can_mask": can_mask})

    config = {"can_filters": can_filters, "single_handle": True}
    if results.interface:
        config["interface"] = results.interface
    if results.bitrate:
        config["bitrate"] = results.bitrate
    bus = Bus(results.channel, **config)

    print('\nConnected to {}: {}'.format(bus.__class__.__name__, bus.channel_info))
    print('Can Logger (Started on {})\n'.format(datetime.now()))
    logger = Logger(results.log_file)
    while keep_going:
        msg = bus.recv(1)
        if msg is not None:
            print(msg)
            logger(msg)
            
    bus.shutdown()
    logger.stop()

def termination_capture(key):
    global keep_going
    if key == keyboard.Key.esc:
        keep_going = False

if __name__ == "__main__":
    keyboard.Listener(on_press=termination_capture).start()
    logCan()