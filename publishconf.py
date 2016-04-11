#!/usr/bin/env python
# -*- coding: utf-8 -*- #

"""Configuration file for publishing to server

This file is imported after :mod:`pelicanconf` when building the site to be
published to the server, rather than for local testing. It overrides several
variables that need to be different when publishing the site, vs. testing it
locally.
"""
from __future__ import unicode_literals

import os
import sys
sys.path.append(os.curdir)

# Import :mod:pelicanconf
from pelicanconf import *

#PATH = 'H:\\VCS\\Repos\\fc-microsites\\SOC 2014'

#: The SITEURL here is the actual URL for the live site. This is used in all the
#: links.
SITEURL = 'http://furmancenter.org/soc2014'

#: When publishing, we want to use absolute URLs (with the full :data:`SITEURL`
#: included), rather than relative URLs
RELATIVE_URLS = False

#: Clear the ``output`` directory so that we have a clean rebuild.
DELETE_OUTPUT_DIRECTORY = True


LOAD_CONTENT_CACHE = True
AUTORELOAD_IGNORE_CACHE = True

#: Some plugins, like ``optimize_images`` can take some time, so we don't want
#: to include them when testing locally, but we do when publishing.
PLUGINS = ['category_meta', 'ordered_categories', 'data_import', 'jinja_tests', 'assets', 'optimize_images']
