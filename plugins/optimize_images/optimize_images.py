# -*- coding: utf-8 -*-

"""
Optimized images (jpg and png)
Assumes that jpegtran and optipng are isntalled on path.
http://jpegclub.org/jpegtran/
http://optipng.sourceforge.net/
Copyright (c) 2012 Irfan Ahmad (http://i.com.pk)
"""

import logging
import os
from subprocess import call
import pdb

from pelican import signals

import sys

logger = logging.getLogger(__name__)

# Display command output on DEBUG and TRACE
SHOW_OUTPUT = False #logger.getEffectiveLevel() <= logging.DEBUG

# A list of file types with their respective commands
COMMANDS = {
    # '.ext': ('command {flags} {filename', 'silent_flag', 'verbose_flag')
    '.jpg': ('{dir}\\jpegtran {flags} -copy none -optimize -outfile "{filename}" "{filename}"', '', '-v'),
    '.png': ('{dir}\\optipng {flags} "{filename}"', '--quiet', ''),
}


def optimize_images(pelican):
    """
    Optimized jpg and png images

    :param pelican: The Pelican instance
    """
    #logger.debug("OPTIMIZING IMAGES")
    #pdb.set_trace()
    '''for path in pelican.settings['PLUGIN_PATHS']:
        sys.path.append(path)
        logger.debug("SYSTEM PATHS: %s" % sys.path)'''
    for dirpath, _, filenames in os.walk(pelican.settings['OUTPUT_PATH']):
        for name in filenames:
            if os.path.splitext(name)[1] in COMMANDS.keys():
                optimize(dirpath, name, cmddir=pelican.settings['PLUGIN_PATHS'][0])

def optimize(dirpath, filename, cmddir):
    """
    Check if the name is a type of file that should be optimized.
    And optimizes it if required.

    :param dirpath: Path of the file to be optimzed
    :param name: A file name to be optimized
    """
    filepath = os.path.join(dirpath, filename)
    logger.info('optimizing %s', filepath)

    ext = os.path.splitext(filename)[1]
    command, silent, verbose = COMMANDS[ext]
    flags = verbose if SHOW_OUTPUT else silent
    command = command.format(filename=filepath, flags=flags, dir=cmddir)
    #logger.debug(command)
    call(command, shell=True)


def register():
    signals.finalized.connect(optimize_images)
