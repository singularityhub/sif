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

# We don't have multiple versions, but can add loading logic here, e.g.
# We also might want (or need) to reload an image based on finding
# a different version.

def get_structure(version=None):
    '''get_structure will return known organization based on a version.
       The versions are organized into the subdirectories here. If the user
       doens't provide a version, we default to SIF_VERSION

       Parameters
       ==========
       version: a version to load, should be a corresponding string (e.g., 02)
    '''

    # Return a simple data structure with what we need
    class SIF:
        HeaderBase = None
        arches = None
        Deffile = None

    # If no provided version, use default
    if version == None:
        version = SIF_VERSION

    if version == "02":
        from .v02 import ( HeaderBase, 
                           arches, 
                           Deffile, 
                           Partition,
                           Signature )

    SIF.HeaderBase = HeaderBase()
    SIF.arches = arches
    SIF.Deffile = Deffile()
    SIF.Partition = Partition()
    SIF.Signature = Signature()
    return SIF
