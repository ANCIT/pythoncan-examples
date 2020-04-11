import can
import cantools

dbc = cantools.database.load_file('/home/ancit/Documents/malai/Antitheft.dbc')
can_bus = can.interface.Bus(bustype='socketcan',channel='vcan0',bitrate=1000000)
tester = cantools.tester.Tester('TransmitNode', dbc, can_bus, None)

tester.start()
status = tester.expect('Ant_VehicleMotion', signals=['Ant_EngineRunning'],  timeout=None, discard_other_messages=False)
print(status)