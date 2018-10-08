# pyW800rf32
Python library to communicate with the W800rf32 devices from
http://www.wgldesigns.com/w800.html

See https://github.com/horga83/pyW800rf32 for the latest version.

Using
=====

Install pySerial first. After that, see the examples in the examples directory.

receive.py usage:
      ./receive.py  <- default /dev/ttyUSB0 baudrate=4800 xonxoff=False

      ./receive.py  <port> <baudrate=n> <xonxoff=True|False>

Receive will create a thread and print X10 codes and command received in the
terminal.