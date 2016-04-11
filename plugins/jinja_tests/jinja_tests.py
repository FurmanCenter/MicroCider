"""Add custom Jinja2 tests to Pelican.

This plugin allows you to specify custom tests (i.e. functions that
return True/False and can be used in Jinja2 templates)
in the config files and then use them in your Jinja2 templates.

Author: Brian Karfunkel (http://bkfunk.github.io)
"""


from pelican import signals

import logging
logger = logging.getLogger(__name__)

def add_tests(generator):
	'''Add the Jinja2 tests specified in the settings to the environment.

	In order add a test, we need to set the Jinja2 environment object's
	``test`` attribute. See the Jinja2 docs on 
	`custom tests <http://jinja.pocoo.org/docs/dev/api/#custom-tests>`_.

	This function relies on a variable being set in the config files, e.g.::

		import filters
		JINJA_TESTS = {'filepath':filters.is_filepath}

	The above would, for example, allow testing to see if a string was a valid
	filepath::

		{% if article.source|filepath %}

	...would call ``filters.is_filepath(article.source)``.
	'''
	generator.env.tests.update(generator.settings['JINJA_TESTS'])


def register():
	'''Attaches the :py:func:`add_tests()` function to the ``generator_init`` signal.'''
	signals.generator_init.connect(add_tests)