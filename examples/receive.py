#!/usr/bin/python3

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

# ############################################################################
# receive.py usage:
#         ./receive.py  <- default /dev/ttyUSB0 baudrate=4800 xonxoff=False
#         ./receive.py  <port> <baudrate=n> <xonxoff=True|False>
#
# Returns hex bytes received, house/unit code and command
# ############################################################################


import sys
sys.path.append("../")

import W800rf32
import time


def print_callback(event):
    print("X10 Housecode: {0}, Unit code: {1}, Command: {2}".format(
            event.device[0],event.device[1:],event.command))

def main():
    print("In main...", sys.argv)

    xon=False
    baud=4800

    if len(sys.argv) >= 2:
        port = sys.argv[1]

        i = 2
        while i < len(sys.argv):
            if 'baudrate' in sys.argv[i]:
                baud = int(sys.argv[i].split('=')[-1:][0])
            if 'xonxoff' in sys.argv[i]:
                if sys.argv[i].split('=')[-1:][0] == 'True':
                    xon = True
            i+=1
    else:
        port = '/dev/ttyUSB0'

    print("Running with ---> Port: {0}, Baud: {1}, Xonxoff: {2}".format(port, baud, xon))
    con = W800rf32.Connect(port, print_callback, debug=True, baudrate=baud, xonxoff=xon)

    print (con)
    while True:
        time.sleep(5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
