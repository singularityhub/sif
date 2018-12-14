
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
from sif.defaults import SIF_VERSION
from struct import ( unpack, calcsize )

class SIFHeader:

    def __init__(self, image, load_header=True, version=None):

        # Load the base for a particular SIF version
        self.load_base(version)

        # We will store global headers, and descriptors
        self.meta = dict()
        self.desc = dict()

        if not os.path.exists(image):
            bot.exit('Cannot find %s.' % image)

        if not self.is_sif(image):
            bot.exit('%s is not a SIF file.' % image)

        bot.info('%s is a SIF file.' % image)
        self.image = image

        # The user might want to wait to load
        if load_header is True:
            self.load_header()


    def __str__(self):
        '''string representation of a SIF image shows the path'''
        return "<SIF:%s>" % self.image

    def __repr__(self):
        '''representation of SIF image is also the path'''
        return self.__str__()


################################################################################
# Printing
################################################################################


    def print_meta(self):
        '''print the metadata for the user to see
        '''
        for key, val in self.meta.items():
            bot.info('SIF Header %s %s' % (key, val) )

    def print_deffile(self):
        '''print the definition file for the user to see
        '''
        for key, val in self.desc['deffile'].items():
            if key != 'deffile':
                bot.info('Deffile %s %s' % (key, val) )

    def print_arch(self):
        '''print the human friendly architecture'''
        if 'arch' in self.meta:
            if self.meta['arch'] in self.arches:
                bot.info('Architecture: %s' % self.arches[self.meta['arch']])


################################################################################
# Validation
################################################################################


    def is_sif(self, image):
        '''determine if an image is SIF based on finding SIF_MAGIC
        ''' 

        with open(image, 'rb') as filey:

            # Skip the first line
            filey.seek(self.base.HdrLaunchLen)

            # Read # of bytes corresponding to length of sif magic
            fmt = "%ss" % self.base.HdrMagicLen

            # Read length of header magic
            line = self.unpack_chars(filey, fmt=fmt)

            if line != None:
                if isinstance(line, str) and line.startswith(self.base.HdrMagic):
                    return True

            return False


    def unpack_chars(self, filey, fmt, number=None, encoding='utf-8', idx=0):
        '''unpack characters, and handle the encoding and removing
           an end character.
        '''
        line = self.unpack_bytes(filey, fmt, number)[idx]

        # Return numbers, otherwise parse bytes to string
        if isinstance(line, (int, float)):
            return line

        return line.decode(encoding).replace(self.base.EndChar, '')


################################################################################
# Loading
################################################################################

    def load_base(self, version=None):
        '''load a sif base, or default to version 02
        '''
        from sif.header import get_structure
        SIF = get_structure(version)

        # We have a header base, arches, and Descriptors
        self.base = SIF.HeaderBase
        self.arches = SIF.arches
        self.Deffile = SIF.Deffile 


    def read_bytes(self, filey, fmt, number=None):
        '''just read a number of bytes from an open file.

           Parameters
           ==========
           filey: an open file object
           number: the number of bytes to read
           fmt: an optional format string
        '''
        if number == None:
            number = calcsize(fmt)

        return filey.read(number)


    def unpack_bytes(self, filey, fmt, number=None):
        '''read AND unpack a number of bytes from an open file. If a 
           format is provided, convert to utf-8 and return the string. 
           If fmt is None, assume a character string of the same length.

           Parameters
           ==========
           filey: an open file object
           number: the number of bytes to read
           fmt: an optional format string
        '''
        byte_values = self.read_bytes(filey, fmt, number)
        return unpack(fmt, byte_values)



################################################################################
# Global Header
################################################################################

            
    def load_header(self):
        '''Once we know is sif, load the header.
        ''' 

        # Start at end of interpreter line, and after sif magix
        byte_start = self.base.HdrLaunchLen + self.base.HdrMagicLen

        with open(self.image, 'rb') as filey:

            # Skip the first line
            filey.seek(byte_start)

            # 1. Read the version
            self.meta['version'] = self.unpack_chars(filey, 
                                                     number=self.base.HdrVersionLen, 
                                                     fmt = "%ss" % self.base.HdrVersionLen)

            # 2. Read the architecture
            self.meta['arch'] = self.unpack_chars(filey, 
                                                  number=self.base.HdrArchLen,
                                                  fmt = "<%ss" % self.base.HdrArchLen)

            # 3. Read the uuid - this returns little endian bytes
            uuid_bytes = self.read_bytes(filey, fmt='<16c')
            self.meta['uuid'] = str(uuid.UUID(bytes_le=uuid_bytes))

            # 4. Read in the remaining Global header fields, 1 signed int
            items = ['ctime', 
                     'mtime', 
                     'dfree',
                     'dtotal',
                     'descroff',
                     'descrlen', 
                     'dataoff', 
                     'datalen']

            for item in items:
                self.meta[item] = self.unpack_bytes(filey, fmt='1q')[0]

            # Load the definition file descriptors
            self.desc['deffile'] = self._load_deffile(filey)


        # Update the user with what was loaded
        self.print_meta()
        bot.newline()
        self.print_arch()
        bot.newline()
        self.print_deffile() 

################################################################################
# Descriptors
################################################################################


    def _load_deffile(self, filey=None, close_file=False):
        ''' load the header descriptor for the definition file. If a file
            object is not provided, open. The fields and format string are 
            provided via the self.Deffile object, which we get from 
            self.header --> __init__.py --> get_structure() --> SIF

            Parameters
            ==========
            filey: an (optional) open file object. We will seek to start of
                   the description offset, if it was read in the global header.
        '''

        # By default, we assume that we will not close the file handle
        close_file = False
 
        # Unless it's not provided, we need to clean up
        if filey == None:
            filey = open(self.image, 'rb')
            close_file = True

        # Read to the description offset
        descriptors = dict()
        filey.seek(self.meta['descroff'])

        # see sif.header module for the default fields and format strings
        values = self.unpack_bytes(filey, self.Deffile.fmt)
         
        # Update the descriptors dictionary
        for d in range(len(values)):
            descriptors[self.Deffile.fields[d]] = values[d]

        # Definition File - offset should point us to the deffile    
        filey.seek(descriptors['Fileoff'])

        # And the length is also provided
        fmt = '%sc' % descriptors['Filelen']
        descriptors['deffile'] = self.unpack_bytes(filey, fmt)

        # Close the file, if wanted
        if close_file is True:
            filey.close()

        return descriptors
