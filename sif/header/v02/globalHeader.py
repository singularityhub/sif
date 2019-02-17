'''

Copyright (C) 2018-2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

The SIF header format is developed and licensed by Sylabs,
see https://github.com/sylabs/sif/blob/master/pkg/sif/sif.go

'''

from sif.logger import bot
from sif.defaults import SIF_VERSION

arches = {
    "00": "Undefined/Unsupported architecture",
    "01": "386 (i[3-6]86) arch code",
    "02": "AMD64 arch code",
    "03": "ARM arch code",
    "04": "AARCH64 arch code",
    "05": "PowerPC 64 arch code",
    "06": "PowerPC 64 little-endian arch code",
    "07": "MIPS arch code",
    "08": "MIPS little-endian arch code",
    "09": "MIPS64 arch code",
    "10": "MIPS64 little-endian arch code",
    "11": "IBM s390x arch code"
}

class HeaderBase:
    '''A SIF Header is a binary header to describe a SIF image, and is defined
       by a set of pre-defined sections and a "SIF_MAGIC" header. See
       https://github.com/sylabs/sif/blob/master/pkg/sif/sif.go for details
    '''
    EndChar           = '\0'
    HdrLaunch         = "#!/usr/bin/env run-singularity\n"
    HdrMagic          = "SIF_MAGIC"
    HdrVersion        = "02"        # SIF SPEC VERSION
    HdrArchUnknown    = "00"        # Undefined/Unsupported arch
    HdrArch386        = "01"        # 386 (i[3-6]86) arch code
    HdrArchAMD64      = "02"        # AMD64 arch code
    HdrArchARM        = "03"        # ARM arch code
    HdrArchARM64      = "04"        # AARCH64 arch code
    HdrArchPPC64      = "05"        # PowerPC 64 arch code
    HdrArchPPC64le    = "06"        # PowerPC 64 little-endian arch code
    HdrArchMIPS       = "07"        # MIPS arch code
    HdrArchMIPSle     = "08"        # MIPS little-endian arch code
    HdrArchMIPS64     = "09"        # MIPS64 arch code
    HdrArchMIPS64le   = "10"        # MIPS64 little-endian arch code
    HdrArchS390x      = "11"        # IBM s390x arch code
    HdrLaunchLen      = 32          # len("#!/usr/bin/env... ")
    HdrMagicLen       = 10          # len("SIF_MAGIC")
    HdrVersionLen     = 3           # len("99")
    HdrArchLen        = 3           # len("99")
    DescrNumEntries   = 48          # default total # available descriptors
    DescrGroupMask    = 0xf0000000         # groups start at that offset
    DescrUnusedGroup  = DescrGroupMask     # descriptor without a group
    DescrDefaultGroup = DescrGroupMask | 1 # first groupid number created
    DescrUnusedLink   = 0                  # descriptor without link to other
    DescrEntityLen    = 256                # len("Joe Bloe <jbloe@gmail.com>...")
    DescrNameLen      = 128                # descriptor name (string identifier)
    DescrMaxPrivLen   = 384                # size reserved for descriptor specific data
    DescrStartOffset  = 4096               # descriptors start after global header
    DataStartOffset   = 32768              # data object start after descriptors

    def __init__(self, updates={}):
        '''a HeaderBase is a pre-set collection of locations and values
            for SIF headers. We use this to parse the header in python
        '''
        for key, val in updates.items():
            self.set_attribute(key, key)    

    def __str__(self):
        return "SIFHeader Version %s" % self.HdrVersion

    def __repr__(self):
        return self.__str__()

    def get_attribute(self, key, default):
        '''get an attribute from the base, or return a default if not defined.

           Parameters
           ==========
           key: the attribute name to get
           default: the default to return
        '''
        if hasattr(self, key):
            return getattr(self, key)
        return default

    def set_attribute(self, key, value):
        '''set an attribute for the base, only if it's already existing.

           Parameters
           ==========
           key: the attribute name to get
           value: the value to set
        '''
        if hasattr(self, key):
            setattr(self, key, value)
