#!/usr/bin/env python
# -*- coding: utf-8 -*- #

"""Main Pelican configuration file

This configuration file is a combination of settings built into Pelican (see
the Pelican documentation `Settings page <http://docs.getpelican.com/en/3.6.3/settings.html>`_),
and custom options for the MicroCider implementation.
"""

from __future__ import unicode_literals
import sys
import os

############################
# Set Theme and Import
# Theme Config File
############################

#: The path to the theme to use to build the site. This is also the location
#: of the :file:`themeconf.py` config file, which is imported into ``pelicanconf``.
THEME = 'themes/SOC'
sys.path.append(THEME)
from themeconf import *


###########################
# Import secret settings
###########################
# Try to import secretconf, but if it fails, just load the sample for testing
sys.path.append(".")
try:
    from secretconf import *
except:
    from secretconf_SAMPLE import *

#: The URL for testing the site. Note that the port number (8000)
#: should match the port specified in fabfile.py
#: This is overridden by the publish config file for actually
#: publishing the site.
SITEURL = 'http://localhost:8000'




###########################
# Basic site settings
###########################

#: Timezone for dates etc. Not really used.
TIMEZONE = 'America/New_York'

#: Default language
DEFAULT_LANG = u'en'

#: Default date format. Not really used.
DEFAULT_DATE = u'fs'

#: Since it's not a blog, we don't want to paginate posts (split across pages)
DEFAULT_PAGINATION = False


############################
# Path Settings
############################
#PATH = 'H:\\VCS\\Repos\\fc-microsites\\SOC 2014'
#PATH = 'J:\DEPT\REUP\SOC\SOC 2014\Microsite Content\content'
#PATH = 'content'
PATH = "../fc-microsites/SOC 2014"
"""
The ``PATH`` is the location of the content. You can set it on the command
line when calling the ``pelican`` command, or you can specify it as an
option when calling ``fabric``.
"""

#: The folder that contains the articles (aka chapters, sections, and slides)
ARTICLE_PATHS = ['report']


#: Folders that contain static content, which doesn't need to be parsed by
#: Pelican. For example, CSV files the just get moved from the content directory
#: to the output directory.
#:
#: Anything that is in these folders will be moved to a folder of the same name
#: in the output directory.
STATIC_PATHS = ['figures', 'data', 'images']


#: Exclude the following directories from the static paths.
#: This means that static files in these directories will not be copied over
#: to the output directory.
STATIC_EXCLUDES = [os.path.join('images', 'backgrounds', 'smaller versions'),
                    os.path.join('images', 'backgrounds', 'originals')]


#: Ignore files that fit a certain pattern. These will not be processed or
#: copied to output.
IGNORE_FILES = ['_*']


############################
# URL/SAVE AS settings
############################
"""
See the main Pelican docs for more on these settings.

Basically, they determine where articles are saved to in the output directory
and also which URLs will be used to view them on the finished site.
"""

#: Chapters and sections are accessible by using the slug name after the
#: site's root URL
CATEGORY_URL = '{slug}/'

#: Where to save the file produced from the ``category.html`` template.
CATEGORY_SAVE_AS = '{slug}/index.html'

# Don't save an authors page or categories page, etc.

#: We do not want to save author pages, since we don't use authors.
AUTHOR_SAVE_AS = ''

#: We do not want an index page for all categories; we will use a custom
#: ``index.html`` template to create our own index page.
CATEGORIES_SAVE_AS = ''

#: We do not use tags
TAG_SAVE_AS = ''

#: We do not use archives
YEAR_ARCHIVE_SAVE_AS = ''

#: We do not use archives
MONTH_ARCHIVE_SAVE_AS = ''

#: We do not use archives
DAY_ARCHIVE_SAVE_AS = ''

#: Each article (i.e. slide) is saved using the article slug within the category
#: which includes the chapter and section. Note that this is for viewing a
#: single slide at a time, which we pretty much only want for sharing purposes;
#: it's nice to be able to direct someone to a single page with a slide, as
#: Facebook, for example, will then put that slide's title in the post, rather
#: than the title for the whole microsite
ARTICLE_URL='{category}/{slug}'

#: Where to save each slide in the output directory
ARTICLE_SAVE_AS='{category}/{slug}.html'

#: Pages are accessed using the slug
PAGE_URL = '{slug}/'

#: Where to save page files
PAGE_SAVE_AS = '{slug}/index.html'


##############################
# Plugins and Extensions
##############################

#: Folders to look for Pelican plugins in
PLUGIN_PATHS = ['plugins']

#: List of plugins to load when testing. We have a different list for publishing
PLUGINS = ['category_meta', 'ordered_categories', 'data_import',
            'jinja_tests', 'assets']
# Requires assets and sass

#: The field that the :py:mod:`ordered_categories` plugin should use to sort
#: chapters and sections by.
CATEGORY_SORT_BY = 'chapterno'



# Add the plugin paths to the system path
for path in PLUGIN_PATHS:
    sys.path.append(path)

import soc_jinja2_filters as filters

#: This matches names of Jinja2 filters to actual methods as defined in
#: :mod:`soc_jinja2_filters`. The keys in this dict are the strings to use
#: in the actual templates (i.e. ``{{ article|debug }}`` will apply the
#: :func:`soc_jinja2_filters.debug` function to the ``article`` object),
#: and the values are the functions that get called when Jinja sees those
#: filters.
JINJA_FILTERS = {'debug':filters.debug,
                'string_list':filters.string_list,
                'cat_level':filters.cat_level,
                'json': filters.json}

#: Test functions to add to the built-in Jinja2 tests. These functions will get
#: called on the objects in the template. So ``{{ article.figure|filepath }}``
#: will call the :py:func:`soc_jinja2_filters.filepath` function on the
#: ``article.figure`` string and return the result.
JINJA_TESTS = {'filepath':filters.filepath}


###########################
# Site-wide external scripts
#############################
#: List of external javascripts to load on each page
SITE_SCRIPTS = [
                # Bootstrap is used for layout, columns, and basic styling like wells
                "//maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js",
                # Proj4.js is needed to reproject some of the geojson files
                "//cdnjs.cloudflare.com/ajax/libs/proj4js/2.3.6/proj4.js",

                # Highcharts is used for figures
                 "//code.highcharts.com/highcharts.js",
                 "//code.highcharts.com/highcharts-more.js",
                 # The data module of highcharts is needed to pull data from HTML tables
                 "//code.highcharts.com/modules/data.js",
                 # The exporting module allows us to export figures as images
                 "//code.highcharts.com/modules/exporting.js",
                 # Highmaps for creating map figures
                  "//code.highcharts.com/maps/modules/map.js",
                  # blazy is a lazy-loading script so that we don't load all the images
                  # for each background immediately
                  "//cdn.jsdelivr.net/blazy/latest/blazy.min.js"]




############################
# DEVELOPMENT ONLY:
############################
#: Overwrite the output directory
DELETE_OUTPUT_DIRECTORY = True
LOAD_CONTENT_CACHE = False


############################
# FEED settings
############################
# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
