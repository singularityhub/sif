#!/usr/bin/env python

# Copyright (C) 2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

from sif.logger import bot
import sys
import os

def main(args):

    lookup = { 'ipython': ipython,
               'python': python,
               'bpython': bpython }

    shells = ['ipython', 'python', 'bpython']

    # The user must supply an image
    if args.image is None:
        bot.exit('You must provide an image to load a SIFHeader client.')

    image = args.image[0]

    # The image must exist
    if not os.path.exists(image):
        bot.exit('Cannot find %s' % image)

    # Present order of liklihood to have on system
    for shell in shells:
        try:
            return lookup[shell](image)
        except ImportError:
            pass
    

def ipython(image):
    '''give the user an ipython shell, optionally load image
    '''
    from sif.main import SIFHeader  
    header = SIFHeader(image)  
    from IPython import embed
    embed()


def bpython(image):
    import bpython
    from sif.main import SIFHeader  
    header = SIFHeader(image)  
    bpython.embed(locals_={'header': header,
                           'image': image,
                           'SIFHeader': SIFHeader})

def python(image):
    import code
    from sif.main import SIFHeader  
    header = SIFHeader(image)  
    code.interact(local={"header": header,
                         'image': image,
                         'SIFHeader': SIFHeader})
