'''
Created on 15-Apr-2020

@author: bk
'''
import struct
import can

def create_message(seatbelt_status):
    return can.Message(arbitration_id=0x010,
                       extended_id=False,
                       data=struct.pack('<HB', seatbelt_status))


def main():
    can.rc['interface'] = 'socketcan'
    can.rc['channel'] = 'vcan0'
    can_bus = can.interface.Bus()

    msg = create_message(0, 0)
    task = can_bus.send_periodic(msg, 1.0)

    while True:
        message = can_bus.recv()

        if message.arbitration_id == 0x022:
            speed = struct.unpack('<H', message.data)[0]
            print('Received motor speed of {} rpm.'.format(speed))
            task.modify_data(create_message(speed, 12))

            if message.data == b'\xff\xff':
                break

    print('Done!')


if __name__ == '__main__':
    main()