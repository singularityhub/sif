
# Copyright (C) 2018 Vanessa Sochat.

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
# License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import uuid
from sif.logger import bot
from sif.header import ( bases, arches )
from sif.defaults import SIF_VERSION
from struct import ( unpack, calcsize )

class SIFHeader:

    def __init__(self, image, load = True):

        # Load the base for a particular SIF version
        self.load_base()
        self.meta = dict()

        if not os.path.exists(image):
            bot.exit('Cannot find %s.' % image)

        if not self.is_sif(image):
            bot.exit('%s is not a SIF file.' % image)

        bot.info('%s is a SIF file.' % image)
        self.image = image

        # The user might want to wait to load
        if load:
            self.load_header()


    def __str__(self):
        '''string representation of a SIF image shows the path'''
        return "<SIF:%s>" % self.image

    def __repr__(self):
        '''representation of SIF image is also the path'''
        return self.__str__()

    def print_meta(self):
        '''print the metadata for the user to see
        '''
        for key, val in self.meta.items():
            bot.info('Found SIF %s %s' % (key, val) )

    def print_arch(self):
        '''print the human friendly architecture'''
        if 'arch' in self.meta:
            if self.meta['arch'] in arches:
                bot.info('Architecture: %s' % arches[self.meta['arch']])

    def load_base(self, version="02"):
        '''load a sif base, or default to version 02
        '''
        self.base = bases.get(SIF_VERSION, version)
 
    def is_sif(self, image):
        '''determine if an image is SIF based on finding SIF_MAGIC
        ''' 

        with open(image, 'rb') as filey:

            # Skip the first line
            filey.seek(self.base.HdrLaunchLen)

            # Read # of bytes corresponding to length of sif magic
            fmt = "%ss" % self.base.HdrMagicLen

            # Read length of header magic
            line = self.unpack_bytes(filey, fmt=fmt)

            if line != None:
                if isinstance(line, str) and line.startswith(self.base.HdrMagic):
                    return True

            return False


    def read_bytes(self, filey, number=None, fmt=None):
        '''read AND unpack a number of bytes from an open file. If a 
           format is provided, convert to utf-8 and return the string. 
           If fmt is None, assume a character string of the same length.

           Parameters
           ==========
           filey: an open file object
           number: the number of bytes to read
           fmt: an optional format string
        '''
        if fmt == None and number == None:
            bot.exit('You must provide a format string OR a number of bytes')

        if fmt == None:
            fmt = "%ss" % number

        elif number == None:
            number = calcsize(fmt)

        return filey.read(number)

    def unpack_bytes(self, filey, number=None, fmt=None, encoding='utf-8'):
        '''read AND unpack a number of bytes from an open file. If a 
           format is provided, convert to utf-8 and return the string. 
           If fmt is None, assume a character string of the same length.

           Parameters
           ==========
           filey: an open file object
           number: the number of bytes to read
           fmt: an optional format string
        '''
        line = self.read_bytes(filey, number, fmt)
        try:
            return self.unpack(fmt, line, encoding)
        except:
            pass

    def unpack(self, fmt, line, encoding='utf-8'):
        '''a wrapper around unpack that handles the encoding and removing
           an end character
        '''
        line = unpack(fmt, line)[0]

        # Return numbers, otherwise parse bytes to string
        if isinstance(line, (int, float)):
            return line

        return line.decode(encoding).replace(self.base.EndChar, '')

            
    def load_header(self):
        '''Once we know is sif, load the header.
        ''' 

        # Start at end of interpreter line, and after sif magix
        byte_start = self.base.HdrLaunchLen + self.base.HdrMagicLen

        with open(self.image, 'rb') as filey:

            # Skip the first line
            filey.seek(byte_start)

            # 1. Read the version
            self.meta['version'] = self.unpack_bytes(filey, 
                                                     number=self.base.HdrVersionLen, 
                                                     fmt = "%ss" % self.base.HdrVersionLen)

            # 2. Read the architecture
            self.meta['arch'] = self.unpack_bytes(filey, 
                                                  number=self.base.HdrArchLen,
                                                  fmt = "<%ss" % self.base.HdrArchLen)

            # 3. Read the uuid - this returns little endian bytes
            uuid_bytes = self.read_bytes(filey, fmt='<16c')
            self.meta['uuid'] = str(uuid.UUID(bytes_le=uuid_bytes))

            # 4. Read in the ctime, 1 signed int
            items = ['ctime', 'mtime', 'ndescr', 'descroff', 'dataoff', 'datalen']
            for item in items:
                self.meta[item] = self.unpack_bytes(filey, fmt='1q')

        # Update the user with what was loaded
        self.print_arch()
        self.print_meta()
