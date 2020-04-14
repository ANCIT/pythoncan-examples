## Installation

By default all Ubuntu installation come with Python2.6.2
Python3 needs to be installed

```shell
sudo apt-get update
sudo apt-get install python3.8
```

Pip3 needs to be installed

```shell
sudo apt-get install python3-pip
```

If you have more than 1 version of Python3 installed in Linux
We need to point Python3 to Python3.8 installation

```shell
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 2
```

```shell
sudo update-alternatives --config python3
```

Running the above command should bring up the list of Python3 installed and show you the automode. Press 2

Few python dependencies that you need to install to continue further. These libraries work in Linux and Windows
Python3 installation would be preferred.

```shell
pip3 install robotframework
pip3 install python-can
pip3 install cantools
pip3 install can-isotp
pip3 install canmatrix
```
# Configuring VCAN [Virtual CAN] in Linux

*   $ sudo modprobe vcan
*   $ sudo ip link add dev vcan0 type vcan
*   $ sudo ip link set up vcan0

Contains Python examples for CAN protocol

can-utils

    candump [Listens to CANBUS]
    cansend [Sends CAN Message on CANBUS]
    cangen [Sends Random CAN Messages on CANBUS]
    cansniffer [Similar to candump]
    canmonitor [Textual UI for candump >> Filter, Clear]

Python >> CAN Raw Message Send and Receive CAN Raw Message Periodic Send

cantools

    It works on DBC / ARXML / KCD
    Load DBC -> Message and Signal
    Send CAN Message using DBC Encoding and Receive thru DBC Decoding thru Python
    candump | cantools
    tester node : Unit Testing : HTML Report

robot framework

    canisotp, cantools, uds
    python : libraries functions
    keyword robot : Language : keyword robot will inturn invoke the python libraries
    test robot : Should follow the syntax of the keyword robot
