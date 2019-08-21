'''
This file is part of pyW800rf32, a Python library to communicate with
the W800 family of devices from http://www.wgldesigns.com/w800.html
See https://github.com/horga83/pyW800rf32 for the latest version.

Copyright (C) 2018  George Farris <farrisg@gmsys.com>

Portions of this code inspired by Edwin Woudt <edwin@woudt.nl>
of the pyRFXtrx project, https://github.com/woudt/pyRFXtrx

pyW800rf32 is free software: you can redistribute it and/or modify it
under the terms of the GNU Lesser General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyW800rf32 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with pyW800rf32.  See the file COPYING.txt in the distribution.
If not, see <http://www.gnu.org/licenses/>.
'''

import setuptools

setuptools.setup(
    name = 'pyW800rf32',
    packages = setuptools.find_packages(),
    version = '0.2',
    description = 'A library to communicate with the W800rf32 family of devices',
    author='George Farris',
    author_email='farrisg@gmsys.com',
    url='https://github.com/horga83/W800rf32',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ' +
            'GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',        
        'Programming Language :: Python :: 3.7',
        'Topic :: Home Automation',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ]
)
