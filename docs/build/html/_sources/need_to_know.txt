
******************************
Tools and Background Knowledge
******************************

.. _about-markdown:

Markdown
========

Most text on a microsite needs to be written in Markdown files, which have the ``*.md`` file extension. `Markdown <https://daringfireball.net/projects/markdown/>`_ is a simple language that is designed to allow you to write plain text files that are readable as text files but can also easily be turned into HTML. For example:

.. code-block:: none

	Header for a Markdown File
	==========================
	 
	Second-Level Header
	-------------------------------
	 
	This is a _markdown_ file. Markdown allows you to:
	* Use normal text
	* Create formatting that doesn't get in the way of readability
	* Create HTML pages without all the markup tags messing everything up

\...would get turned into:

.. code-block:: html

	<h1>Header for a Markdown File</h1>
	 
	<h2>Second-Level Header</h2>
	 
	<p>This is a <em>markdown</em> file. Markdown allows you to:</p>
	 
	<ul>
	<li>Use normal text, while still allowing you to use:
	<ul><li>Nested lists</li>
	<li>Links</li>
	<li>Even tables</li></ul></li>
	<li>Create formatting that doesn't get in the way of readability</li>
	<li>Create HTML pages without all the markup tags messing everything up</li>
	</ul>

Pelican, which is the framework that MicroCider uses to build microsites from raw input files, uses Markdown with an extra twist: at the beginning of files, **metadata** can be included by putting the name of a variable (or *field*) at the start of the line, followed by a colon, followed by what the contents of that variable should be. (See `the Pelican docs <http://docs.getpelican.com/en/3.6.3/content.html>`_ for more information.)

For example, suppose we had a blog and we wanted to create a post with a title, an author, and a date, as well as some actual text content:

.. code-block:: none
	:name: example_md_blog_post
	:caption: blog_post1.md
	:linenos:

	title: This is the title of the post
	author: Brian
	date_created: 2016-12-30 09:00
	 
	This is the _content_ of the post. Note the blank line above, which is required, 
	as it tells Pelican where the metadata ends and where the actual content begins.
	 
	This is a second paragraph of content. Again, a blank line in between! But we 
	can use **Markdown** in the content. We can also include <b>normal HTML</b>.

.. note::

	Note that the ``date_created`` variable name doesn't have a space, because otherwise it would not work as a variable (they cannot contain special characters, either).

Pelican first reads ``blog_post1.md``, parsing all the metadata and other contents and storing the information in a Python object, ``article``, which has attributes like ``title`` (containing the string "This is the title of the post"), ``author``, etc. It also has a ``content`` attribute, which contains the actual content of the blog post, which is everything after the first blank line (i.e. line 4).

We will go over the format of the Markdown files that MicroCider is looking for in the :ref:`Microsite Content <microsite-content>` section.

.. note::

	In general, **not all metadata fields need to be included**. If ``blog_post1.md`` did not have an ``author`` field, for example, ``article.author`` would just return ``None``. Be aware that in some cases, however, that may cause an error (for example, Pelican **requires** the ``title`` field, and will throw an error if an article does not have a title).

	You can almost always, however, add fields that are not used without any issues.

.. note::

	The metadata fields need to come at the **beginning** of the Markdown file, but the fields themselves do not need to come in any order.


Jinja2
=======

When Pelican is creating the HTML file to display that blog post, it will use a *template file*, which is written using a language called `Jinja2 <http://jinja.pocoo.org/>`_, which is basically HTML with some Python inserted into it. Pelican (also written in Python), will look for a place in that template to put the title, the author, etc. For example, the template might include the following (note that ``{{ ... }}`` is how we tell Jinja2 to insert the value of the variable inside):

.. code-block:: html+jinja
	:name: example_jinja2_template
	:caption: post.html
	:linenos:

	<h1>{{ article.title }}</h1>
	<h3>Written by {{ article.author }}</h3>
	<em>Created on: {{ article.date_created }}</em>
	<h4>Filed under: <strong>{{ article.topic }}</strong></h4>
	<div class="content">{{ article.content }}</div>

So, when Pelican wants to create an HTML file for :ref:`blog_post1.md <example_md_blog_post>`, it first reads the Markdown file, creates a Python object from the contents of that file, and then it tries to fill in the blanks:

.. code-block:: html
	:caption: blog_post1.html
	:linenos:
	:emphasize-lines: 1, 3, 4, 5, 10

	<h1>This is the title of the post</h1>
	<h3>Written by Brian</h3>
	<em>Created on: 2016-12-30 09:00</em>
	<h4>Filed under: <strong></strong></h4>
	<div class="content"><p>This is the <em>content</em> of the post. Note the blank line
	above, which is required, as it tells Pelican where the metadata ends and where the 
	actual content begins.</p>
	 
	<p>This is a second paragraph of content. Again, a blank line in between! But we can
	use <strong>Markdown</strong> in the content. We can also include <b>normal HTML</b>.</p></div>

Let's break down some of what went on:

- Line 1: For the article title, it simply got inserted in place of the ``{{ article.title }}`` statement.
- Line 3: Notice that the ``date_created`` was inserted without any sort of processing: Pelican has no way to know it's a *date*, so it just sees it as a normal string. If you wanted to display it as, say, "Dec. 30, 2016", you would need to change your template or tell Pelican to parse that field as a date.
- Line 4: ``blog_post1.md`` didn't have a ``topic`` field, so nothing was inserted into the ``<strong></strong>`` tags on line 4. This doesn't cause a problem, but it doesn't look great. We might want to rewrite the template so that it first tests to see if there are any topics associated with a post before including anything:

	.. code-block:: html+jinja

		{% if article.topic %}<h4>Filed under: <strong>{{ article.topic }}</strong></h4>{% endif %}

	That way, if ``article.topic`` returns ``None``, the ``h4`` tag won't be inserted at all, so there will just be a blank line.

- Lines 5-10: Pelican, in reading in the Markdown, inserted ``<p>`` paragraph tags around each paragraph of the article content. It also replaced ``_content_`` on line 5 with the HTML version: ``<em>content</em>``, and similarly changed ``**Markdown**`` on line 10 to ``<strong>Markdown</strong>``.

Another feature of Jinja2 templates is that they can import and extend other template files. So, for example, we use ``base.html`` to be the base template for all the other templates; much of the output pages needs to be the same (they all need to load certain scripts, they all need to set the stylesheets, have ``<html>`` and ``<body`` tags, etc.) so we can put the boilerplate in ``base.html`` and then each other template simply includes those pieces that are different for each type of content.

Part of the extension/importing feature is the use of **blocks**, which allow you to put a placeholder for certain content that can be overwritten or changed. For example, in ``templates/base.html``, we have the following in the ``<head>`` tag:

.. code-block:: html+jinja

	<title>{% block title %}{{ SITENAME|striptags }}{% endblock title %}</title>

Normally, then, the title of every page would be the site name (set in the ``SITENAME`` variable in the config files, and removing any HTML tags). However, if we had a template that inherited from ``base.html`` but we wanted to change the title, we could just write:

.. code-block:: html+jinja

	{% block title %}My New Template Title{% endblock title %}

Notice, in particular, that we do not repeat the ``<title>`` tag, since the contents of the title block get inserted into that tag, replacing whatever was there before.

.. seealso::
	
	`Jinja docs on template inheritance <http://jinja.pocoo.org/docs/dev/templates/#template-inheritance>`_

Python
========

Pelican, as well as the plugins we use, are written in Python. Jinja2 syntax is Python-like; basically it is Python but very limited, and without any reliance on indenting.

Javascript
==========
