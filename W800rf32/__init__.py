# This file is part of pyW800rf32, a Python library to communicate with
# the W800 family of devices from http://www.wgldesigns.com/w800.html
# See https://github.com/horga83/pyW800rf32 for the latest version.
#
# Copyright (C) 2018  George Farris <farrisg@gmsys.com>
#
# Portions of this code inspired by Edwin Woudt <edwin@woudt.nl>
# of the pyRFXtrx project, https://github.com/woudt/pyRFXtrx
#
# pyW800rf32 is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyW800rf32 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pyW800rf32.  See the file COPYING.txt in the distribution.
# If not, see <http://www.gnu.org/licenses/>.

"""
This module provides the base implementation for pyW800rf32
"""

# from __future__ import print_function

from time import sleep
import threading
import sys
import serial
from . import lowlevel


###############################################################################
# W800rf32Event class
###############################################################################

class W800rf32Event:
    """ Abstract superclass for all events """

    def __init__(self, event):
        self.device = event.device
        self.command = event.command


###############################################################################
# W800rf32Transport class
###############################################################################

class W800rf32Transport:
    """ Abstract superclass for all transport mechanisms """

    # pylint: disable=attribute-defined-outside-init
    @staticmethod
    def parse(data):
        """ Parse the given data and return an W800rf32Event """
        if data is None:
            return None
        # return with DecodeW800Packet object with x10 device and command
        decoded_obj = lowlevel.parse(data)
        if decoded_obj is not None:
            event = W800rf32Event(decoded_obj)
            return event
        return None

    def reset(self):
        """ reset the W800rf32 device """
        pass

    def close(self):
        """ close connection to W800rf32 device """
        pass


###############################################################################
# PySerialTransport class
###############################################################################

class PySerialTransport(W800rf32Transport):
    """ Implementation of a transport using PySerial """

    def __init__(self, port, debug=False, baudrate=4800, xonxoff=False):
        self.debug = debug
        self.port = port
        self.baud = baudrate
        self.xon = xonxoff
        self.serial = None
        self._run_event = threading.Event()
        self._run_event.set()
        self.connect()

    def connect(self):
        """ Open a serial connexion """
        try:
            self.serial = serial.Serial(self.port, baudrate=self.baud,
                                        xonxoff=self.xon, timeout=0.1)
        except serial.serialutil.SerialException:
            print("Can't open port -> ", self.port)
            print("Exiting...")
            sys.exit(1)

    def receive_blocking(self):
        """ Wait until a packet is received return with an W800rf32Event """
        data = None
        while self._run_event.is_set():
            try:
                data = self.serial.read(4)
            except TypeError:
                continue
            except serial.serialutil.SerialException:
                import time
                try:
                    self.connect()
                except serial.serialutil.SerialException:
                    time.sleep(5)
                    continue
            if not data or data == '\x00':
                continue
            buffer = bytearray(data)
            if self.debug:
                print("W800rf32: Recv: " +
                      " ".join("0x{0:02x}".format(x) for x in buffer))
            return self.parse(buffer)

    def reset(self):
        """ Reset the W800rf32 """
        sleep(0.3)
        self.serial.flushInput()

    def close(self):
        """ close connection to W800rf32 device """
        self._run_event.clear()
        self.serial.close()


class Connect:
    """ The main class for w800rf32.py.
    """
    def __init__(self, device, event_callback=None, debug=False,
                 transport_protocol=PySerialTransport,
                 baudrate=4800, xonxoff=False):
        self.baud = baudrate
        self.xon = xonxoff
        self._run_event = threading.Event()
        self._run_event.set()
        self.event_callback = event_callback

        self.transport = transport_protocol(device, debug, baudrate=self.baud,
                                            xonxoff=self.xon)
        self._thread = threading.Thread(target=self._connect)
        self._thread.setDaemon(True)
        self._thread.start()

    def _connect(self):
        """Connect """
        self.transport.reset()

        while self._run_event.is_set():
            event = self.transport.receive_blocking()
            if isinstance(event, W800rf32Event):
                if self.event_callback:
                    self.event_callback(event)

    def close_connection(self):
        """ Close connection to W800rf32 device """
        self._run_event.clear()
        self.transport.close()
        self._thread.join()
