.. _microsite-content:

*****************
Microsite Content
*****************

.. sidebar:: Contents

  .. contents:: Structure
    :depth: 3

The content files for a microsite are arranged in the following folder structure::

    CONTENTROOT/
      ├─data/
      │   ├─maps/
      │   │   └─[map files]
      │   │
      │   └─[data files]
      │
      ├─figures/
      │   └─[figure files]
      │
      ├─images/
      │   ├─backgrounds/
      │   │   └─[background images]
      │   │
      │   ├─figures/
      │   │   └─[downloaded images of figures (optional)]
      │   │
      │   └─theme/
      │       └─[icons, logos, favicon, etc.]
      │
      ├─pages/
      │   └─[page *.md files]
      │
      └─report/
          └─[report text]


We will discuss each of the above folders below.

.. note::

    The ``CONTENTROOT`` folder can be whatever you want; you just need to specify its location in the :py:const:`PATH` variable defined in the ``pelicanconf.py`` config file. It may be convenient to have the content be another repository from the main MicroCider repository; that way, people can work on the content pages without having to worry about all the particulars of MicroCider, and without endangering the main MicroCider code.

.. caution:: **Pasting Text and Typography**

  Much of the content text may be copied from other formats like PDF or PowerPoint. Make sure you clean up any text copied from PDF, in particular, or any other pasted text, so that you replace curly apostrophes and quotes with the HTML equivalent:

  =========== ========================
  ``&rquo;``  curly right double quote
  ``&lquo;``  curly left double quote
  ``&rsquo;`` curly apostrophe or right single quote
  ``&lsquo;`` curly left single quote
  ``&amp;``   ampersand (&)
  =========== ========================


===========
Report Text
===========

The report text is organized into *chapters*, which are composed of *sections*, which are sets of *slides*. The text is contained in :ref:`Markdown <about-markdown>` files that are grouped into sections and chapters based on the directory structure. For example, here is part of the structure for the 2014 SOC microsite::

    report/
      ├─focus/
      │   ├─index.md            <-- focus chapter's index file
      │   ├─changes/
      │   │   ├─index.md        <-- changes's index file, which is by default the intro slide
      │   │   ├─changes1.md     <-- First CONTENT slide of changes section, in focus chapter
      │   │   ├─changes2.md
      │   │   └─...more slides...
      │   │
      │   ├─context/
      │   │  ├─index.md
      │   │  ├─context1.md
      │   │  ├─context2.md
      │   │  └...
      │   │
      │   └─...more sections...
      │
      └─overview/
          ├─index.md
          ├─landuse/
          │   ├─index.md
          │   ├─landuse.md
          │   ├─landuse.md
          │   └─...
          │
          ├─homeowners/
          │   ├─index.md
          │   ├─homeowners1.md
          │   ├─homeowners2.md
          │   └─...
          │
          └─...more sections...


You can of course rename the chapters and sections whatever you want, and you could rename the slides, although it is convenient to name them with the section name and a number, to ensure they are sorted in the order you want.

Notice that each chapter and each section have a file called ``index.md``. These files define metadata about the chapter/section, such as the title, the short version of the title to be displayed on the left-hand bar, the order in which to sort each chapter/section, etc. This functionality is not built into Pelican, but is added by a combination of the :ref:`category_meta <category_meta>` plugin and the :ref:`ordered_categories <ordered_categories>` plugin.

.. note::

    Remember that, in Pelican's terminology, both **chapters** and **sections** are "categories" -- or more properly, categories and subcategories, respectively).

Slides
------

A *slide* is the basic unit of content. MicroCider is designed to display one slide per page. As you scroll through the site, you move from slide to slide. A slide can have just text (for example, an introduction slide), or can have text next to a *figure*, which can be an image or something interactive like a graph or a map.

Each slide is defined by a Markdown file with the slide's ``slug``, which is a short way of referring to that piece. Slugs should not have spaces or special characters.

.. note::

    Slugs are used in the URL, and generally to identify an article (aka a slide), a category (aka a section or chapter), or a page. For example, in the 2014 SOC, the "Focus on Density" chapter has the slug ``focus``, and the URL for that chapter is http://furmancenter.org/soc2014/focus/.

.. _slide_layout:

Layout of a Slide's Markdown File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is an example of a slide's Markdown file

.. code-block:: none
    :caption: ...\\report\\focus\\changes\\changes1.md

    title: NYC lost almost a million people in the 1970s. But since 1980, its population has grown steadily.
    shortname: Population Growth
    background: images/backgrounds/StraphangersBW.jpg
    background_copyright: View Apart / Shutterstock
    figure: changes1_nyc_pop_1970_2010.js
    data: changes1_nyc_pop_1970_2010.csv
    mapdata:
    figure_title: New York City Population
    figure_subtitle:
    figure_sources: Sources: U.S. Census, Neighborhood Change Database, NYU Furman Center
    figure_notes:
    layout: figure-right

    By 2010, the city’s population reached an all-time high. And the latest estimates
    suggest the city continues to grow, suggesting the population has reached 8.4 million.

    Despite its notorious housing affordability challenges, New York City remains a highly
    desirable place to live, and people continue to move here.

Here are all the fields in a slide file:

:title:
    The slide's title, which is displayed as a header. It is usually in the form of a complete sentence (or sentences) that describes the finding succinctly.

:shortname:
    The short name is what is displayed on the navigation bar on the left. It should be very short (no more than a few words), and should just describe what the finding is about, not what the finding *is*

:background:
    The location of the background image file, relative to the root of the microsite (the root is, for example, the folder that contains the report folder). You can also use a color, e.g. ``rgb(255, 255, 155)``

:background_copyright:
    The text to display with the copyright information for the background image

:figure:
    The file location for the figure to accompany the slide. If this is blank or missing, then the slide will default to use a ``no-figure`` layout (see below), unless another layout is specified. MicroCider will look for the figure file in the ``figures`` folder within the root directory.

    .. note::

        The figure can be an image file, in which case the image is displayed, or a javascript file, in which case an empty container for the figure is created on the page, and the javascript file is imported to fill the container.

        While generally we use the Highcharts library to create figures, the javascript file that is called here could do anything you want (create a custom figure using d3.js, for example, or do something completely different).

        Also, you can use a URL instead of a file reference, in which case an ``<iframe>`` will be inserted; this is useful if you want to embed a figure from another location.

    .. note::

        **Multiple Figures**

        For multiple figures, each figure's script file path should be separated by a pipe character (``|``), without spaces in between. The figures will be displayed in tabs ordered in the same way they are in the Markdown file. Similarly, include each figure's title, subtitle, sources, notes, etc., separated by pipes. Make sure the order of the titles, for example, is the same as the order for the figure script file paths. Also, if one figure doesn't have a subtitle, for example, make sure to leave a blank space (i.e. ``Subtitle for figure 1||Subtitle for figure 3``).

:data:
    The CSV file to load containing the raw data. MicroCider looks for this in the ``data`` folder of the root directory. Once found, it will load the CSV file, create an HTML table with the data, and put it into the page (although the table will be hidden from view, it will be in the HTML code, and viewable by, for example, a screen reader for someone with visual disabilities). We will see below that the standard Highcharts figures will load the data from that HTML table, rather than reading in the CSV itself.

:mapdata:
    If this is a map, the ``mapdata`` field is where you would put the base map. For example, if you were doing a choropleth (area heat map) for community districts, the path to the geojson file with the CD map would go in ``mapdata``, and a CSV with CD numbers and the values you want to map would go in ``data``.

    .. note::

        If you are making a bubble map, then you will want to use *two* geojson files: one for the underlying map of New York (e.g. a borough map), and the other for the individual points being mapped with bubbles. In that case, you put *both* paths in ``mapdata``, but you separate them with a pipe character (``|``), without spaces.

:figure_title:
    The title for the figure. Note that this will override any title specified in the figure's javascript file itself.

:figure_subtitle:
    The figure's subtitle, if any

:figure_sources:
    The sources line to go beneath the figure. This should include the "Sources: " or "Source: " text.

:figure_notes:
    Any additional notes to go below the sources line.

:layout:
    The slide's layout, which can be:

    - ``no-figure``
        Default if no ``figure`` specified

    - ``figure-right``
        Slide title and text on the left, figure on the right

    - ``figure-bottom``
        Slide title on the upper left, text on the upper right, figure across the bottom

    - ``figure-bottom-wide``
        Like figure-bottom, but extra wide

    - ``map-right``
        Slide title and text on the left, map on the right. Map slides are slightly wider than figure slide by default.

    .. note::

        The ``layout`` field can be the name of any template file in the ``templates\slide-templates`` folder. So if you want to tweak or add a layout, just add a new template to that folder, and put that template's filename (without the ``.html`` extension) here.

    .. seealso::

        :ref:`templates`

:content (field name is implicit!):
    The remainder of the text is stored in the slide's ``content`` attribute

    .. note::

      Anything after a blank line is put into the ``content`` attribute, even if it is of the ``fieldname: value`` form. All fields must be at the start of the file, with no blank lines between them, or else they won't be parsed by Pelican.


Sections
--------

Slides are grouped into sections. Each section has a name, and by default an intro slide (although that can be disabled). The ``index.md`` file in that section's folder both defines metadata for the section itself (such as which order it should appear in within the chapter) and is the content markdown file for the intro slide.

.. code-block:: none
    :caption: ...\\report\\focus\\changes\\index.md

    title: Changes in New York City's Density
    shortname: Changes in NYC's Density
    chapterno: 1.02
    hide_intro_slide: False
    background: images/backgrounds/NightStreet.jpg
    background_copyright: Shutterstock / littleny

    The typical New Yorker in 2010 lived in a less dense neighborhood than in 1970, even
    though the 2010 population is higher.

The section ``index.md`` file serves double duty: it defines metadata about the section itself, and by default it is the Markdown file for the introduction slide for that section.

.. topic:: Section Metadata

  These fields define the metadata for the section itself, which will affect how all the slides in the section are arranged on the site.

  :title:
    The title for the section's intro slide

    .. warning::

      The ``title`` field is **required**, even if the intro slide is being hidden. Without it, Pelican won't even process the index.md file, and will not display the slides in that section.

    .. note::

      The ``title`` field can include Markdown formatting, as well as HTML. For example, here is the title field for the ``landuse`` section of the ``overview`` chapter from 2014:

        .. code-block:: html
          :caption: ...\\report\\overview\\landuse\\index.md

          title: <span class="text-accent">The State of</span><br>Land Use and the Built Environment

      The theme config file ``themeconf.py`` sets which fields will be parsed for Markdown formatting, by setting the ``FORMATTED_FIELDS`` variable.

  :shortname:
    This is what is displayed on the left-hand navigation bar.
  :chapterno:
    This determines how the section is ordered within the category.

    .. note::

      The name of the field used for sorting can be changed in the ``pelicanconf.py`` config file by changing the ``CATEGORY_SORT_BY`` field. The sorting field need not be numeric; categories will be sorted using the default sorting behavior of Python, so for example strings will be sorted alphabetically.

    .. caution::

      Although we use a number, in the form ``[chapter number].[zero-padded section number]``, so that each section (aka subcategory) is in order both within it's chapter (aka category) and within the project as a whole, technically that is not required. So, for example, the ``focus`` chapter could have ``chapterno: 1`` and then the ``changes`` section could have ``chapterno: 2``, and things would be sorted the same way. Having an absolute ordering, though, does make things clearer and saves you from having to look at multiple files to know where a section fits in the whole report.

  :hide_intro_slide:
    If set to ``True``, will not create an introduction slide. If this is not specified, or set to be anything other than ``True``, then there will be an intro slide; you don't need to explicitly set it to ``False``.

    .. note::

      **Alternatives to Default Introduction Slide**

      Even if you *do* want an introduction slide, that doesn't mean you need to use the section's ``index.md`` file to define it. You can set ``hide_intro_slide: True`` and then, for example, create a ``changes0.md`` file, or any other Markdown file with a name that will be ordered before any of the other slides.


.. topic:: Introduction Slide

  These fields define the introduction slide for the section, which by default is inserted before any other content slides in the section. It is just a normal slide, so for example if you wanted you could put a figure on the intro slide, or attach data, etc. Normally, however, there is just some basic text and a title. Refer to the :ref:`normal slide layout <slide_layout>` for all the fields that can be specified. Because the ``shortname`` field applies to the section itself, there is one additional field which allows you to define the short name for the introduction slide:

  :intro_shortname:
    If set to anything other than blank, will be used instead of "Introduction" for the left side bar.


Chapters
--------

Chapters are groups of sections. You can think of a chapter as a single column of slides. You move pretty seamlessly from one section to the next just by scrolling down, but to go to the next chapter you have to load a new page. Note that having lots of slides in a single chapter can make it take a long time to load the page, so longer reports should be split into at least a couple chapters.

Unlike section ``index.md`` files, chapter ``index.md`` files are only used for metadata, and not for an actual slide. So there are usually only three fields that are relevant: the ``title`` field, which is required, the ``shortname``, and the ``chapterno``. Here is an example from the 2014 SOC:

  .. code-block: none
    :caption: ...\\report\\focus\\index.md

    title: <span class="text-accent">Focus on</span> Density
    shortname: Focus on Density
    chapterno: 1.0

.. note::

  By default, the chapters are represented by icons, so the ``title`` field is not used except in setting some metadata for when the page is shared. The icons are specified by the :data:`themeconf.CHAPTER_LINK_IMAGES` option in the ``themeconf.py`` config file.

.. tip:: **Hiding the left-hand nabar**

  The ``hide_navbar`` field, when set to ``True``, will hide the left-hand navigation bar, even on large screens, and will make the content of that chapter or section take up the full width of the screen. Note that this can only be set on the top-most category on the page. For example, at ``http://furmancenter.org/soc2014/focus/``, if the ``focus`` chapter's ``hide_navbar`` was set to true, then it wouldn't matter what the value of ``hide_navbar`` was for the sections within the ``focus`` chapter; the navbar is either hidden or not for the entire page.

  Similarly, if ``focus/index.md`` did *not* hide the navbar, it would not matter if ``focus/changes/index.md`` *did* hide it, at least when viewing ``http://furmancenter.org/soc2014/focus/``. On ``http://furmancenter.org/soc2014/focus/changes``, however, where the ``changes`` section is the top-most category, then the navbar *would* be hidden.


.. note:: **The Data Map**

  The 2014 SOC microsite's Data chapter shows how flexible the MicroCider framework can be. Here is an excerpt of the code in ``report/datamap/index.md``:

  .. code-block:: none
    :caption: ...\\report\\datamap\\index.md

    title: City, Borough, and Community District Data
    shortname: Data
    chapterno: 3.0
    hide_navbar: true
    background: images\backgrounds\SubwayExitBW.jpg
    background_copyright: littleny / Shutterstock
    figure: datamap_static.js
    figure_title: Click on Community District to View Data Profile
    figure_sources:
    figure_notes: &nbsp;
    layout: map-right
    mapdata: maps/nyc_cds_simple1k_proj.geojson

    As part of each year's report, we compile current and historical statistics
    for over 50 housing, neighborhood, and socioeconomic indicators at the city,
    borough and community district levels.

    [content continues...]

  By using ``hide_navbar``, we make the *chapter* look like a *page*. We don't have any sections, and we make the ``index.md`` slide the entire chapter. This is an example of how the same markdown file will be interpreted differently based on where it is in the file tree, and how everything, to Pelican, is an "article".

-------------------------------------------------

=====
Pages
=====

Pages are outside of the chapters/sections/slides framework. Each page is displayed on its own; while slides are designed to take up a single screen, so scrolling moves you from slide to slide, pages can be as long as you want, and scrolling will scroll down the page. The canonical type of page would be an "About" page, that describes the report or organization.

Pages are located in the ``pages`` folder of the content root. They can have many of the fields that `slides`_ can have, including figures, backgrounds, etc. Here is an example from the 2014 SOC about page:

.. code-block:: none
  :caption: ...\\pages\\about.md

  title: About the _State of New York City&rsquo;s Housing and Neighborhoods in 2014_ Report
  shortname: About
  background: images/backgrounds/StraphangersBW.jpg
  background_copyright: View Apart / Shutterstock

  The _State of New York City&rsquo;s Housing and Neighborhoods_ report, published annually by the
  NYU Furman Center, provides a compendium of data and analysis about New York City&rsquo;s housing,
  land use, demographics, and quality of life indicators for each borough and the city&rsquo;s 59
  community districts.

  The report combines timely and expert analysis of NYU Furman Center researchers with data transparency.
  You can read the full published [2014 report](http://furmancenter.org/research/sonychan/2014-report)
  on our website, and you can access [the latest version of the report, and our
  [archives](http://furmancenter.org/research/sonychan), as well.

  [content continues...]


=====
Data
=====

Data files are stored as CSVs. The :mod:`data_import` plugin reads the CSVs and then inserts them as hidden HTML tables in each slide. This allows screen readers to have access to the data (for people with visual disabilities), and also allows for the CSVs to be written into the HTML file so they don't have to be loaded separately, which can take more time. The figures will then pull the data from the HTML table and parse it into Javascript objects.

It is best to make the CSV file as simple as possible; remove any extraneous data columns or rows, and simplify column headers, etc. Make sure that numbers are stored as numbers (i.e. they don't have quotes around them -- this can particularly happen when there are commas separating the 1,000s place in numbers), and that strings with spaces in them *do* have quotes around them.

Maps
----

Maps are a particular case for data. There are two kinds of maps that we typically display:

- Choropleth maps (sometimes called "heat maps" or "shaded area maps")
    These are maps with areas for each geography (e.g. each community district, or each census tract), which are shaded according to the value of a variable within that geography. For example, police precincts colored by the crime rate within that precinct.

    For these maps, there is a **map file**, which has information about the geographies themselves (that is, the actual shapes of each geography, as well as things like names, identifiers, etc.), and a **data file**, which contains the data values for each geography. To make the map, we **join** the data to the map file. This is very similar to the process in GIS: you load a data table (in our case, a CSV), and use some variable to join each data value to a particular shape on the map.

    Since we only use a handful of geography levels, we can put a single map file for each level (precinct, school district, borough, community district, SBA), and multiple figures can use those map files.

- Bubble/point maps
    These are maps where individual points are displayed on top of a **base map**; in the case of bubble maps, those points are represented by circles that are sized based on a value for that point. For example, our building permits maps display the location of each building permit with circles that have a radius set based on the number of units authorized by that permit.

    These maps have *two* map files: the **base map file**, which is usually something like the borough map, since it is just used as the background, and the **point data file**, which contains both the locations of all the points *and*, in the case of bubble maps, the value we want to use to size the bubbles.

Regardless of the type of map, all map files should be placed in the ``data\\maps\\`` folder, and figures that reference these files should reference them in relation to the maps folder, e.g. ``mapdata: maps/nyc_sbas2010_simplify1k_proj.geojson``.

.. seealso::

  :ref:`Working with Maps <working-with-maps>`


=======
Figures
=======

Figures can be javascript files, image files, or links to embeddable content.

======
Images
======

Background Images
-----------------

Most slides will have a background image. Make sure these images are as small as is reasonable.

Figure Images
-------------

For Facebook sharing, you may want to download each figure as an image, and place it here. That way, sharing an individual slide should have the image for that slide, rather than an image for the whole report. This is optional.

Theme Images
------------

These are images like the logo, and the chapter link images. Also, the `favicon`, which is the little icon that shows on the tab/window header when viewing a page.
