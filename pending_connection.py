from test.UdsTest import UdsTest
from udsoncan.connections import *
from test.stub import StubbedIsoTPSocket
import socket
import threading
import time
import unittest

try:
    _STACK_UNVAILABLE_REASON = ''
    _interface_name = 'vcan0'
    import isotp
    import can
    s = isotp.socket()
    s.bind(_interface_name,rxid=1,txid=2)
    s.close()
    _STACK_POSSIBLE = True
except Exception as e:
    _STACK_UNVAILABLE_REASON = str(e)
    _STACK_POSSIBLE = False

class TestIsoTPSocketConnection(UdsTest):

    def setUp(self):
        self.tpsock1 = StubbedIsoTPSocket(timeout=0.1)
        self.tpsock2 = StubbedIsoTPSocket(timeout=0.1)

    def test_open(self):
        conn = IsoTPSocketConnection(interface='vcan0', rxid=0x001, txid=0x002, tpsock=self.tpsock1, name='unittest')
        self.assertFalse(conn.is_open())
        conn.open()
        self.assertTrue(conn.is_open())
        conn.close()
        self.assertFalse(conn.is_open())

    def test_transmit(self):
        conn1 = IsoTPSocketConnection(interface='vcan0', rxid=0x100, txid=0x101, tpsock=self.tpsock1, name='unittest')
        conn2 = IsoTPSocketConnection(interface='vcan0', rxid=0x101, txid=0x100, tpsock=self.tpsock2, name='unittest')
