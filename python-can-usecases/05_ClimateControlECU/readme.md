#CLIMATE_CONTROL_ECU

## messages and signals
1. Vehicle_simulation_data
    a. vehicle_speed
    b. engine_speed.
 2. climate_simulation_data
    a. indoor_temperature
 3. climate_control_signal
    a. Ac status
    

## Functionality
The climate ECU, gives the vehicle speed as a periodic message. It checks for the indoor temperature of the car. It set the AC status, according to the indoor temperature of the car.

## Pre-conditions
 To set the virtual can, use the following command:
 	sudo modprobe vcan
	sudo ip link add vcan0 type vcan0
	sudo ip link set vcan0 up
 

## Use cases
The vehicle speed is always taken into consideration. However, this does not affect the AC status. The indoor temperature of the car is read. If the temperature is lesser that 25, the AC shall be turned OFF, else the AC status is turned ON.



 

