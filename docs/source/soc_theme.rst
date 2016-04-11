.. _soc-theme:

*************
The SOC Theme
*************

Most of the MicroCider secret sauce is in the SOC theme, which is a `Pelican theme <http://docs.getpelican.com/en/3.6.3/themes.html>`_. As documented in the Pelican documentation, the SOC folder is split into two subfolders: ``static``, which contains static assets like stylesheets and scripts, and ``templates``, which contains Jinja2 templates for displaying microsite content.

``static`` Contents
===================

The ``static`` folder contains CSS files, javascript files, and web fonts.

``css``
--------

MicroCider uses `Sass <http://sass-lang.com/>`_ (i.e. "syntactically awesome style sheets") to split CSS into several components (i.e. *`partials <http://sass-lang.com/guide#topic-4>`_*). The stylesheets are written in SCSS, which is an extension of CSS that allows for things like variables and calculations. For example, we create colors as variables, and those variables are used in a number of style declarations, so we can then change the color scheme by just changing how we set those variables, and the changes will be propogated throughout.

Note that wwe use the `assets <https://github.com/getpelican/pelican-plugins/tree/master/assets>`_ Pelican plugin to automatically compile the Sass code into one CSS file (``style.css``) every time the site is generated. The relevant code is in the ``base.html`` template file::

	<!-- Custom Stylesheet -->
	{# We use the assets plugin to compile all the CSS on the fly #}
	{% assets filters="scss", output="css/style.css","css/style.scss" %}
	<link rel="stylesheet" href="{{ SITEURL }}/{{ ASSET_URL }}">
	{% endassets %}

In general:

* ``_colors_and_fonts.scss``

.. _templates:

``js``
-------

``grouped_categories``
~~~~~~~~~~~~~~~~~~~~~~~

A Highcharts module that allows for grouping categories on the x-axis of a chart. For example, you can have each borough and then within each borough bars for two different years.

``figures.js``
~~~~~~~~~~~~~~~

A script that has code to handle figures.

.. js:function:: setHighchartsOptions()

  Sets default options for Highcharts, so that charts look consistent site-wide. These options can generally be overridden by setting the options in specific figure scripts.

  In particular, this includes the :js:data:`colors` array, which defines the color scheme for figures and maps.

.. js:function:: getFigureText(chart)

  :param chart: The Highcharts chart object to get text for
  :returns: An object with two attributes:

              - ``title`` containing HTML for both the figure title and subtitle (since they are both inserted into the chart's ``title``, as we use the ``subtitle`` for the footnote)
              - ``footnote`` containing the HTML for the sources and notes for the figure, which ultimately gets inserted into the ``subtitle`` attribute of the figure

  This function returns the title, subtitle, sources, and notes for a given figure,
  pulling them from the ``<caption>`` tags of the data table, where they are stored after
  having been read in from the markdown files.

  This allows us to set all of the text in Markdown files that can be more easily edited than figure script files. The figure title, for example, gets parsed by Pelican in the slide Markdown file, then gets put into the page in the ``<caption>`` tag, and then gets read by this function from the HTML and inserted into the Highcharts ``title`` attribute.

.. js:function:: group2Cols(parent_cat, child_cat)

  :param array parent_cat: The parent category (aka supercategory), as a column of the parsed data table
  :param array child_cat: The child category, as a column of the parsed data table

  This function takes two columns and converts them into the format required by
  ``grouped-categories.js``:

  .. code-block: javascript
    :caption: Format expected by ``grouped-categories``

    [{
        name: "Parent category name",
        categories: ["child", "category", "values"]
    }, {
        name: "Second Parent category name",
        categories: ["other", "values"]
    }]


  ``parent_cat`` is an array representing the column of values for the parent category
  (aka supercategory).

  ``child_cat`` is an array representing the column of values for the child category.

  This function assumes the columns are laid out as they would be to make a stacked
  bar graph in Excel, namely:

  =======================  ========================

  "Parent Category Name"    "Child Category Name"
  "Parent value 1"            "Child value 1"
  null                        "Child value 2"
  "parent Value 2"            "Child value 1"
  null                        "Child value 2"
  =======================  ========================

  So, the parent category is ``null`` whenever that row's child value is part of the
  same parent category; in this case, we need to turn this into:

  .. code-block: javascript

    [{
        name: "Parent value 1",
        categories: ["Child value 1", "Child value 2"]
    }, {
        name: "Parent value 2",
        categories: ["Child value 1", "Child value 2"]
    }]


.. js:function:: groupColumns(columns, groupedIndices)

  :param array columns: An array of column arrays, as you would get in the ``parsed`` function in Highcharts
  :param array groupedIndices:

  Function to take column array and create a grouped categories array

.. js:function:: resizeAll()

  This function resizes all the figures to be the height of their parent.

  This allows the actual size of the slides to be set at runtime, while the
  figures will be expanded to fit them.

  Note that right now it assumes a full-screen layout; we assume for example
  that ``.slide-figure-right`` is actually on the right, rather than having wrapped
  around to be on the bottom, as happens if the screen is not wide enough.

  TODO: Need to do the resizing differently for small screens


Templates
============


The template defines each slides *structure*, and it *may* define actual content, too. For example, suppose the template for a page had the following::

	<h1>Welcome to {{ page.title }}</h1>

The "Welcome to" would appear on every page created with that template, but the special double-braces ``{{`` and ``}}`` are a directive to Jinja2 to insert the contents of the ``title`` attribute of the ``page`` object, so the text following "Welcome to" would be different for each page.

.. autojinja: macros.html

.. autojinja: base.html

.. autojinja: macros


.. autojinja: macros.in
