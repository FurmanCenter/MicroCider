***************************
Introduction to MicroCider
***************************

MicroCider is a framework for creating static microsites to publish data-driven narratives. It is built on `Pelican <http://docs.getpelican.com/en/3.6.3/>`_. 

It combines text files, written in `Markdown <https://daringfireball.net/projects/markdown/>`_, figures (images or interactive figures created with Javascript, particularly the `Highcharts <http://www.highcharts.com/>`_ charting library), data (in CSV files), and background images to create a scrollable microsite, split into multiple chapters. The resulting site will be output into a directory, and it can then simply be copied and pasted onto a web server to make the site live!

What MicroCider Is
==================

MicroCider allows you to create static data-driven microsites without having to set up any sort of content management system (CMS) (Wordpress, etc.). You take static files on your computer, process them with MicroCider, and the output can be moved to a web server to produce a live site -- no database needed!

Most of the content, furthermore, can be created by non-technical staff, as it's just text files written in Markdown. Using the Highcharts and Highmaps libraries, basic figures can be created with only a minimal knowledge of Javascript. And if you don't want interactive figures, you can just use static images, or even embedded figures created on sites like CartoDB or Plot.ly.

MicroCider is designed for projects that may need to be created iteratively, but which to not need to change much once they are released; if you need to dynamically update the content, then a full-fledged CMS may be what you need. MicroCider was created by the `NYU Furman Center <http://www.furmancenter.org/>`_ to easily publish reports that are chock full of data. To get a sense of what MicroCider can do, check out the Furman Center's :emphasis:`State of New York City's Housing and Neighborhoods` `report <http://stateofthecity.furmancenter.org/>`_.


Putting the Pieces Together
===========================

At its simplest, MicroCider is a program that looks in various places for various pieces, chops them up, and puts them back together as a website. The inputs to this process are pieces of **content**, and the **output** is the microsite itself. MicroCider is the machine that turns content into output, and it does so by using Pelican and then making some changes to how Pelican works.


.. topic:: :ref:`Microsite Content <microsite-content>`

    The *content* is primarily the components that change from microsite to microsite. Namely:

    + Report Text
        The report text contains the main narratives.

        * Slides
            The basic unit of content. Think of it like a slide in PowerPoint: usually a title, some text, and then sometimes a figure or image.

        * Sections
            Slides are grouped into sections. Multiple sections can be in the same HTML file (i.e. the same page of the website, not to be confused with *pages* below).

        * Chapters
            Sections are grouped into chapters, where each chapter is a separate webpage on the microsite.

    + Pages
        Pages are distinct pieces of content that are not in the chapters/sections/slides heirarchy. The canonical example is the "About" page; it doesn't fit into any narrative.

    + Images
        Every slide has a background image. In addition, there are images for things like the logo, and the index page.

    + Figures
        Slides can have figures, which can be interactive (e.g. created by a Javascript file using something like Highcharts.js), or images. They can also be embedded figures from other sites (e.g. CartoDB).

    + Data
        Data files are mostly CSVs, which are then embedded into the HTML files that are output, and used by interactive figures. There are also map files, which are in the geojson format.

.. topic:: MicroCider

    MicroCider determines how to interpret the content, how to use it to build web pages, and how to display and style those pages. Most of the functionality of MicroCider comes from Pelican. The key things that MicroCider itself adds are:

    + :ref:`SOC Theme <soc-theme>`
        The theme determines how the content is output into webpages.

        * Templates
            Templates are sort of like MadLibs: they say "put the page title here", and then MicroCider fills in the blanks for each piece of content. The templates are written in Jinja2, which is HTML with pieces of Python-like code embedded into it.

        * Static Files
            These are "static" because, unlike templates, they do not change based on which page is being written, but are the same for the whole site. The primary examples are CSS stylesheets and scripts (i.e. Javascript files) that handle things like sharing a slide on social media, for example.

    + :ref:`Plugins <plugins>`
        Pelican plugins are pieces of Python code that change the way Pelican behaves. For example, we have a plugin that allows you to set the order that chapters appear on the front page; by default, Pelican will order everything alphabetically. Some of these are unique to MicroCider, but others were created by other developers.



The Mechanics of MicroCider and Pelican
=======================================

MicroCider determines how to interpret the content, how to use it to build web pages, and how to display and style those pages. Most of the functionality of MicroCider comes from Pelican. Pelican works by reading all the content (see above), and building Python objects from that; for example, each page, which is written in Markdown, gets parsed and turned into a ``page`` object, with *attributes* like ``title``, ``url``, ``content``. Some of those attributes are specified in the Markdown file itself, like ``title``, but others are generated by Pelican, such as ``url``, using settings in certain configuration files as well as things like the location of the Markdown file in the directory tree (so, for example, ``chapter1\sectionA\slideA1.md`` has a ``url`` of ``http://the.site.domain/chapter1/sectionA/slideA1.html``).

The key things that MicroCider itself adds are:

- :ref:`SOC Theme <soc-theme>`
    Once Pelican has constructed Python objects from the content, the `theme <http://docs.getpelican.com/en/latest/themes.html>`_ determines how those objects get turned into a website. Pelican themes have two main parts:

    + Templates
        These are HTML files written in `Jinja2 <http://jinja.pocoo.org/docs/dev/templates/>`_. Basically they are HTML with bits of Python-like code in there to do some basic processing and manipulation. You can think of it like HTML *MadLibs*: the template might say "put title here", and then for every slide, MicroCider will insert that slide's title there. Templates are described in much more depth later on.

    + Static Files
        These are "static" because, unlike templates, they do not change based on which page is being written, but are the same for the whole site. The primary examples are CSS stylesheets, which tell the browser how to style the different components of each webpage, and javascript files (aka *scripts*) that are included on every webpage of the microsite.

        .. note::
            The Javascript files that define the figures that go on each slide are part of the **content**, not the theme; the theme's Javascript files are for things like default settings, handling window resizing, etc.

- :ref:`Plugins <plugins>`
    Pelican `plugins <http://docs.getpelican.com/en/latest/plugins.html>`_ are pieces of Python code that alter the way that Pelican behaves. While the **theme** affects how the Python objects Pelican creates are turned into webpages, **plugins** manipulate these objects *before* (well, usually before) they get to the theme stage. For example, Pelican does not come with the ability to sort chapters other than alphabetically, so we use a plugin, ``ordered_categories`` to allow us to sort chapters explicitly.


*A Note on Terminology*
-----------------------

Pelican was built for blogs, so the terminology it uses is different from the terminology we use. In particular, the basic unit of content for Pelican is an **article**. Each article belongs to a single **category**.

We use a plugin called :py:mod:`category_meta` which extends categories to allow subcategories as well. 

+-------------+------------+----------------------------+
| Pelican     | MicroCider | SOC 2014 Examples          |
+=============+============+============================+
| category    | chapter    | - **Focus**                |
|             |            | - **Citywide Overview**    |
+-------------+------------+----------------------------+
| subcategory | section    | - Focus > **Drivers of     |
|             |            |   Density**                |
|             |            | - Citywide Overview >      |
|             |            |   **Renters and Their      |
|             |            |   Homes**                  |
+-------------+------------+----------------------------+
| article     | slide      | - Focus > Drivers of       |
|             |            |   Density > **"Housing     |
|             |            |   Unit Increases"**        |
|             |            | - Citywide Overview >      |
|             |            |   Renters and Their Homes  |
|             |            |   > **"Rent Burden"**      |
+-------------+------------+----------------------------+
| page        | page       | About page                 |
+-------------+------------+----------------------------+









