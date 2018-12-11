
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
from sif.logger import bot
from sif.header import ( bases, arches )
from sif.defaults import SIF_VERSION
from struct import unpack

class SIFHeader:

    def __init__(self, image):

        # Load the base for a particular SIF version
        self.load_base()
        self.meta = dict()

        if not os.path.exists(image):
            bot.exit('Cannot find %s.' % image)

        if not self.is_sif(image):
            bot.exit('%s is not a SIF file.' % image)

        bot.info('%s is a SIF file.' % image)
        self.image = image
        self.load_header()
        self.print_meta()


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
            number = self.base.HdrMagicLen

            # Read length of header magic
            line = self.read_bytes(filey, number = number, 
                                   fmt = '%ss' % number)

            if line != None:
                if isinstance(line, str) and line.startswith(self.base.HdrMagic):
                    return True

            return False


    def read_bytes(self, filey, number, fmt, encoding='utf-8'):
        '''read a number of bytes from an open file. If a format is provided,
           convert to utf-8 and return the string.

           Parameters
           ==========
           filey: an open file object
           number: the number of bytes to read
           fmt: an optional format string
        '''
        line = filey.read(number)
        try:
            line = unpack(fmt, line)[0]
            return line.decode(encoding).replace(self.base.EndChar, '')
        except:
            pass


    def load_header(self):
        '''Once we know is sif, load the header.
        ''' 

        # Start at end of interpreter line, and after sif magix
        byte_limit = 512
        byte_start = self.base.HdrLaunchLen + self.base.HdrMagicLen

        with open(self.image, 'rb') as filey:

            # Skip the first line
            filey.seek(byte_start)

            # 1. Read the version
            self.meta['version'] = self.read_bytes(filey = filey, 
                                                   number = self.base.HdrVersionLen,
                                                   fmt = "%ss" %self.base.HdrVersionLen)

            # 1. Read the architecture
            self.meta['arch'] = self.read_bytes(filey = filey, 
                                                number = self.base.HdrArchLen,
                                                fmt = "%ss" %self.base.HdrArchLen)
            self.print_arch()

