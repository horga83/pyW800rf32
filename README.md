# pyW800rf32
Python library to communicate with the W800rf32 devices from
http://www.wgldesigns.com/w800.html

See https://github.com/horga83/pyW800rf32 for the latest version.

I wrote this to support X10 devices for Home Assistant.  These devices work:

RSS18 4 unit keypads, BRIGHT/DIM keys mapped to unit 4 ON/OFF

KR19A keychain remote

MS16A Motion sensor

Others may work, test with the receive.py program in examples.

Using
=====

Install pySerial first. After that, see the examples in the examples directory.

receive.py usage:

      ./receive.py  <- default /dev/ttyUSB0 baudrate=4800 xonxoff=False
      ./receive.py  <port> <baudrate=n> <xonxoff=True|False>

Receive will create a thread and print X10 codes and command received in the
terminal.
