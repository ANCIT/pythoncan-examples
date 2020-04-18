import can
import cantools
from pynput import keyboard
import threading

db = cantools.db.load_file('climate_ecu.dbc')
#can_bus = can.interface.Bus(bustype='socketcan',channel='vcan0',bitrate=1000000)
can_bus = can.interface.Bus(bustype='socketcan',channel='vcan0',bitrate=250000)

climate_simulation_MSg = db.get_message_by_name('climate_simulation_data')
climate_Control_MSg = db.get_message_by_name('climate_control_signal')


def on_press(key):
    print("Key Event Identified")
    try:
        if key.char == 'a': # handles if key press is a
                # Message : climate_simulation_data
                data = climate_simulation_MSg.encode({'indoor_temp':0})
                message = can.Message(arbitration_id=climate_simulation_MSg.frame_id, data=data, is_extended_id=False)
                try:
                    can_bus.send(message)
                    print("Set Temp : 0")
                    #print(" climate_simulation_data Message sent on {}".format(can_bus.channel_info))
                except can.CanError:
                    print("Message NOT sent")
        if key.char == 'b': # handles if key press is a
                # Message : climate_simulation_data
                data = climate_simulation_MSg.encode({'indoor_temp':30})
                message = can.Message(arbitration_id=climate_simulation_MSg.frame_id, data=data, is_extended_id=False)
                try:
                    can_bus.send(message)
                    print("Set Temp : 30")
                    #print(" climate_simulation_data Message sent on {}".format(can_bus.channel_info))
                except can.CanError:
                    print("Message NOT sent")
    except AttributeError:
        print(" Unknown Key Event")


def on_Key():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
    
if __name__ == '__main__':
    on_Key()