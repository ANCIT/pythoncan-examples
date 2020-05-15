# -*- coding: UTF-8 -*-
#.Data:2018/5/19

import CANoe
import time
import configparser
import os

#Read User Configuration
config = configparser.RawConfigParser()
config.read('usecase02_configuration.properties')
configurationPath = config.get('TESTCONFIGURATION', 'configurationpath')
print(configurationPath)
testspec = config.get('TESTCONFIGURATION', 'testspecification')
print(testspec)
# if len(testspec) != 0:
#     updateTestSpecification(configurationPath, testspec) 

app = CANoe.CANoe() #定义CANoe为app

app.open_simulation(configurationPath) #导入某个CANoe congif

if len(testspec) != 0:
    app.load_testsetup(testspec)
    
 
app.start_Measurement() #启动CANoe
app.start_testmodule()
time.sleep(120)
app.stop_Measurement() #停止CANoe
