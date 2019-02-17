'''

Copyright (C) 2018-2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from sif.logger import bot
from sif.utils import ( 
    get_userhome, 
    read_json, 
    getenv,
    convert2boolean 
)
import tempfile
import os
import sys


#########################
# Caches
#########################

USERHOME = get_userhome()
SIF_VERSION = getenv("SIF_VERSION", "02")

# Singularity Cache
_cache = os.path.join(USERHOME, ".singularity")
SINGULARITY_CACHE = getenv("SINGULARITY_CACHEDIR", default=_cache)

# Temporary Storage
SIF_TMPDIR = os.environ.get('SIF_TMPDIR', tempfile.gettempdir())
