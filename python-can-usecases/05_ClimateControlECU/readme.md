
# Climate control ECU

# List of messages and signals
    1.vehicle_simulation_data
       a. vehicle_speed
       b. engine_speed
    2. climate_simulation_data
       a. indoor temperature
    3. climate_control_signals
       a. ac_status
  
#Expectations
   On receiving the data from the climate_simulation_data about the temperature of the car, the AC is either turned 'ON' or "OFF' accordingly. 
   

# Use case
   1. The temperature of the car is 18 deg. Thus the AC can be turned OFF.
   2. The temperature of the car is 30 deg. Thus the AC is turned ON.
   3. The Vehicle speed is a cyclic message.
    
 



