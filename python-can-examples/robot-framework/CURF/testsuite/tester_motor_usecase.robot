*** Settings ***
Resource      ../keywords/curf.robot
Test Setup      Set CAN Bus ${INTERFACE} ${CHANNEL} ${BITRATE} ${DB FILE} 
Test Teardown   End Log Can 
Library    DateTime

*** Variables ***
${DB FILE}              /home/ancit/git/pythoncan-examples/python-can-examples/can-examples/system_MainBus.dbc
${INTERFACE}            socketcan
${CHANNEL}              vcan0
${BITRATE}              500000
${DEFAULT TIMEOUT}      3
${DEFAULT NODE}         DRIVER


*** Test Cases ***
Check the reception of a CAN signal 01
    Check CAN Signal MSSpeed Equals To 0 TimeOut ${DEFAULT TIMEOUT} Seconds   
    
Send a given signal 01
    Send Signal MCSpeed With Value 50
    
Check the reception of a CAN signal 02
    Check CAN Signal MSSpeed Equals To 50 TimeOut ${DEFAULT TIMEOUT} Seconds 
   
Send a given signal 02
    Send Signal MCSpeed With Value 0
    
Check the reception of a CAN signal 03
    Check CAN Signal MSSpeed Equals To 0 TimeOut ${DEFAULT TIMEOUT} Seconds  
   
Send a given signal 04
    Send Message MotorControl Signal MCSpeed With Value 45
    
Send a given signal 03
    Send Signal MCSpeed With Value 65535
    

    
