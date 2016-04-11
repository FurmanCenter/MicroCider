"""Configuration file for the theme.

This is imported by the main configuration files.
"""

############################
# General Site Settings
############################

#: Author, not really used
AUTHOR = u'NYU Furman Center'

#: The main branding text
SITENAME = u"State of New York City's <br>Housing &amp; Neighborhoods in 2014"

#: Site description (used in meta tags)
SITEDESC = u"The NYU Furman Center's annual report on New York City and its neighborhoods."

#: This is the default image to share to Facebook
DEFAULT_IMAGE = "images/figures/overview_landuse_landuse1.png"

#############################
# Stylesheet import settings
#############################
#: List of external CSS stylesheets to load
CSS_URLS = ["//maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css",
			"//cdn.jsdelivr.net/jquery.gray/1.4.2/gray.min.css"]


############################
# Theme Settings
############################
#: Static path in the theme folder. The contents of this folder will be copied
#: to the output directory. It normally includes things like CSS stylesheets,
#: site-wide javascript files, etc.
THEME_STATIC_PATHS = ['static']

# We use the assets plugin to compile Sass into css on the fly
# but uncomment this if you want to use a static CSS file instead
#CSS_FILE = 'theme/css/style.css'

############################
# Themed brand/identity images
# These are in the content folder images/theme
############################

#: The site logo. This path is with respect to the content path (i.e. PATH)
BRAND_IMAGE = 'images/theme/FurmanCenter_Icon_CMYK_TranspOrange.png'

#: List of images to use for chapter links, both on the index page and in the
#: top navbar. Any chapters without images will just have the chapter name as
#: the link.
CHAPTER_LINK_IMAGES = ['images/theme/Density.png',
					'images/theme/CitywideOverview.png',
					'images/theme/Data.png']

#: Location of the favicon, relative to the content directory (i.e. PATH)
FAVICON = 'images/theme/favicon.ico'


#: These are templates that are processed directly, without any content like
#: articles, pages, etc. Basically, they are templates that do not receive any
#: objects created by Pelican except for the default objects.
#: In our case, the only page we want to render directly is the index page
#: (i.e. the home page for the microsite).
DIRECT_TEMPLATES = ('index')



#: This tells Pelican to use the filename to set the article slug. The slug will
#: be the filename without the extension.
SLUGIFY_SOURCE = 'basename'

#: Within sections, sort articles (i.e. slides) by slug (as opposed, for example
#: to by date, which doesn't make sense in our context). Slugs will be sorted
#: alphabetically.
ARTICLE_ORDER_BY = 'slug' # Sort articles by the slug (i.e. alphabetically)

#: Which metadata fields can have markdown formatting (or HTML) in them
FORMATTED_FIELDS = ['title','summary']

#: Scripts within the theme's static folder that should be loaded onto every
#: page. Note that these are paths relative to the output directory; by defaut
#: all the files in the :py:data:`THEME_STATIC_PATHS` directories are saved
#: into the ``/theme/`` subfolder of the output directory.
THEME_SCRIPTS = ["/theme/js/grouped_categories/grouped-categories.js",
			"/theme/js/figures.js",
			"/theme/js/scripts.js"]

############################
# SOC Theme Settings
############################
#: The default layout for slides. Note that if there is a figure specified,
#: whatever it is, the :py:data:`DEFAULT_FIGURE_LAYOUT` will be used instead.
#: The layout is simply the name of a template in the ``slide-templates`` folder
DEFAULT_LAYOUT = 'no-figure'

#: The default layout to use for slides with non-empty ``figure`` fields.
DEFAULT_FIGURE_LAYOUT = 'figure-right'

#: Notes to go on every figure. NB: If you set DEFAULT_FIGURE_NOTES to be
#: non-empty, specifying the notes on any specific figure will OVERRIDE the
#: default; if you want the default PLUS specific notes, you have to manually
#: insert the default into the specific figure's markdown file.
DEFAULT_FIGURE_NOTES = ""

#: A list of the images to cycle through for the background if none is specified
#: on a particular slide
DEFAULT_BACKGROUNDS = ["images/backgrounds/BklynBridge.jpg", "images/backgrounds/BKNavyYard.jpg"]


#: The path that the :py:mod:`data_import.data_import` Pelican plugin should
#: look in for data files.
DATA_PATH = 'data'
