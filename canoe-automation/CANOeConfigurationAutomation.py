# -*- coding: UTF-8 -*-
#.Data:2018/5/19

import CANoe
import time


import configparser
import os

config = configparser.RawConfigParser()
config.read('usecase02_configuration.properties')
configurationPath = config.get('TESTCONFIGURATION', 'configurationpath')
print(os.path.isfile(configurationPath))
testspec = config.get('TESTCONFIGURATION', 'testspecification')
 
f = open(configurationPath, "r+")
data = ""
print(type(data))
for x in f:
    if "<VFileName V7 QL>" in x :
        if ".tse" in x:
            print(x)
            data +="<VFileName V7 QL> 1 " + testspec + "\n"
        else :
            data += x
    else :
        data += x
 
f.close()
 
file1 = open(configurationPath,"w")#write mode 
file1.write(data) 
file1.close() 

app = CANoe.CANoe() #定义CANoe为app

# path = '"'+configurationPath+'"'
# print(path)
 
app.open_simulation(configurationPath) #导入某个CANoe congif
 
app.start_Measurement() #启动CANoe
 
# app.stop_Measurement() #停止CANoe
