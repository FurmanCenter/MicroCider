"""
This module includes Jinja2 filters used in the SOC theme,
expanding the set of manipulations that can be performed within
templates.

See the Jinja2 documentation for more information on filters.

"""

import os
import json as json_mod



def json(obj):
	'''Output an object ``obj`` as JSON object.

	:returns: The ``obj`` as a JSON string, or an empty dict if ``obj`` can't
				be converted using :py:func:`json.dump()`.

	.. note::
		If you want to view the contents in the source, it's best to follow
		this filter with the built-in ``pprint`` `filter <http://jinja.pocoo.org/docs/dev/templates/#pprint>`_.

	'''
	try:
		res = json_mod.dump(obj)
		return res
	except:
		return {}


def debug(obj, verbose=False):
	'''Output ``obj`` as a dict, allowing for easy debugging.

	If ``obj`` has no ``__dict__`` method, then it is returned unaltered.
	Otherwise, it returns a tuple with the name of ``obj`` and then the dictionary.
	By default, the values attached to dictionary's ``settings`` and ``_context`` keys
	are set to be empty to avoid cluttering the result with extraneous information.

	:param obj: The object to be output. Usually it will be an object
				passed by Pelican, such as ``article`` or ``category``
	:param verbose: If ``True``, return the full contents of the ``settings`` and ``_context``
					keys, which Pelican includes in a lot of passed objects but which tend
					to have less useful information.

	:returns: A tuple with the object's ``title`` attribute (if it exists, or else
				the ``name`` attribute, or else ``obj.__str__``) and then the (cleaned)
				contents of ``obj.__dict__``. If ``obj`` doesn't have a ``__dict__`` attribute,
				then returns the object itself.
	'''
	if hasattr(obj, '__dict__'):
		d = obj.__dict__.copy()
		if not verbose:
			d['settings'] = ''
			d['_context'] = ''
		return (getattr(obj, 'title', None) or getattr(obj, 'name', None) or str(obj), d)
	else:
		return obj


def string_list(obj, index=None):
	'''Filter to make a string into a list by splitting on pipe (``|``).

	For things like multiple figures, MicroCider uses pipe-delimited lists within
	the metadata fields in the content Markdown files; the contents of that metadata
	field can be a single figure, or else multiple figures separated by the pipe character.

	This filter converts such a string into a list (which is a list of length 1 if the string
	does not contain any pipe characters), and returns that list or, if an ``index`` has been
	specified, returns the :literal:`index`:emphasis:`th` element of that list.

	:param str obj: A string object
	:param int index: An index to return a single element of the list

	:returns: A list with each component of the string, or else a single element (if ``index``
				included). If the list does not contain the index ``index``, nothing is returned.

	'''
	if index is None:
		return obj.split('|')
	else:
		try:
			return obj.split('|')[index]
		except:
			pass


def cat_level(obj, level=0, minlevel=None, maxlevel=None):
	'''Returns the category level of an object (unused)'''
	lvl = getattr(obj, 'level', None)
	if lvl:
		if lvl == level or \
			((minlevel is None or lvl >= minlevel) and \
			(maxlevel is None or lvl <= maxlevel)):
			return obj


def filepath(string):
	'''Test for whether a string is a filepath.

	This is not a filter, but a `test <http://jinja.pocoo.org/docs/dev/templates/#tests>`_.

	:param string: the string to test

	:returns: ``true`` if ``string`` can be split into a file path and extension; false otherwise
	'''
	fname, fext = os.path.split(string)
	return fext and len(fext) > 0