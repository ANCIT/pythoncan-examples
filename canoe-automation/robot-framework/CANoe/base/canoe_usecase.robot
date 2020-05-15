*** Settings ***
Resource   canoe_keyword.robot
Library    DateTime

*** Variables ***
${CONFIGURATIONPATH}    E:/ancit-projects/canoe-autoit/CentralLockingSystem/CentralLockingSystem.cfg
${TESTSPECIFICATION}    E:/ancit-projects/canoe-autoit/CentralLockingSystem/TestSetup.tse


*** Test Cases ***
Load Simulation and Run TestSetup
    Open Simulation    ${CONFIGURATIONPATH}
    Load TestSetup    ${TESTSPECIFICATION}
    # Load TestSetup    ${TESTSPEC2}
    Start Measurement
    Start TestModule
    # Waiting    90
    # Stop Measurement
    
# Run TestSetup
    # Start Measurement
    # Start TestModule
    
   
# Load and Run TestSetup
    # Load TestSetup    ${TESTSPEC2}    
    # Start Measurement
    # Start TestModule
    