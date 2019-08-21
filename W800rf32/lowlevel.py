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
This module provides low level packet parsing and generation code for the
W800rf32.
"""


hcodeDict = {
    0b0110: 'A', 0b1110: 'B', 0b0010: 'C', 0b1010: 'D',
    0b0001: 'E', 0b1001: 'F', 0b0101: 'G', 0b1101: 'H',
    0b0111: 'I', 0b1111: 'J', 0b0011: 'K', 0b1011: 'L',
    0b0000: 'M', 0b1000: 'N', 0b0100: 'O', 0b1100: 'P'}


# End up here with a packet of data.
# Parse the data packet, check length and take last 4 bytes if longer than 4
def parse(data):
    """ Parse a packet from a bytearray """
    #if data[0] == 0 or len(data) < 4:
    if len(data) < 4:
        # null length packet - sometimes happens on initialization
        return None

    # take only last 4 bytes
    expected_length = 4

    if len(data) > expected_length:
        data = data[-4:]

    # Check for valid data
    if data[0] + data[1] != 0xFF or data[2] + data[3] != 0xFF:
        return None

    obj = DecodeW800Packet()

    # return house and unit code as well as command
    obj.get_x10code_and_cmd(data)
    return obj


#############################################################################
# DecodeW800Packet class
#
# If we have what looks like a valid data packet, decode it into house, unit
# code and command
#############################################################################

class DecodeW800Packet():

    def __init__(self):
        """Constructor"""
        super(DecodeW800Packet, self).__init__()
        self.device = None
        self.command = None

    # dig out the house and unit code and the command
    def get_x10code_and_cmd(self, data):
        """Load data from a bytearray"""

        xb3 = "{0:08b}".format(data[0])  # format binary string
        b3 = int(xb3[::-1], 2)  # reverse the string and assign to byte 3
        xb1 = "{0:08b}".format(data[2])  # format binary string
        b1 = int(xb1[::-1], 2)  # reverse the string and assign to byte 1

        # Get the house code
        house_code = hcodeDict[b3 & 0x0f]
        # Next find unit number
        x = b1 >> 3
        x1 = (b1 & 0x02) << 1
        y = (b3 & 0x20) >> 2
        unit_number = x + x1 + y + 1

        self.device = "{0}{1}".format(house_code, unit_number)

        # Find command
        # 0x19 and 0x11 map to dim and bright but we don't support dim  and
        # bright here so we map it to the illegal unit code "0". 0x11 and
        # 0x19 will not map correctly on all keypads.  4 unit keypads will
        # have units 1 to 3 correct but unit 4 will be 4 for "on" but 5 for
        # "off".  Five unit keypads will be opposite, 5 will be "on" and 4
        # will be "off" but we already have a 4 "off".
        if b1 == 0x19:
            self.command = 'Off'
            # self.unit_number = 0
        elif b1 == 0x11:
            self.command = 'On'
            # self.unit_number = 0
        elif b1 & 0x05 == 4:
            self.command = 'Off'
        elif b1 & 0x05 == 0:
            self.command = 'On'
