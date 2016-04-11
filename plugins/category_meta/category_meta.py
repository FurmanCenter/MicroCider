'''Copyright 2014, 2015 Zack Weinberg

Category Metadata
-----------------

A plugin to read metadata for each category from an index file in that
category's directory.

For this plugin to work properly, your articles should not have a
Category: tag in their metadata; instead, they should be stored in
(subdirectories of) per-category directories.  Each per-category
directory must have a file named 'index.ext' at its top level, where
.ext is any extension that will be picked up by an article reader.
The metadata of that article becomes the metadata for the category,
copied over verbatim, with three special cases:

 * The category's name is set to the article's title.
 * The category's slug is set to the name of the parent directory
   of the index.ext file.
 * The _text_ of the article is stored as category.description.
'''

'''
.. note::

    This version of Category Metadata has been edited to work for the particular needs
    of MicroCider. In particular, we added the next/previous/parent/children aspects.

Expanded Category Metadata
--------------------------


Category meta filters articles for index.ext
When found, sets categories

Ordered categories adds super-categories to categories

Supercategories need articles (subcategories).

'''



from pelican import signals
import os
import re
import logging
import copy
logger = logging.getLogger(__name__)

### CORE BUG: https://github.com/getpelican/pelican/issues/1547
### Content.url_format does not honor category.slug (or author.slug).
### The sanest way to work around this is to dynamically redefine each
### article's class to a subclass of itself with the bug fixed.
###
### Core was fixed in rev 822fb134e041c6938c253dd4db71813c4d0dc74a,
### which is not yet in any release, so we dynamically detect whether
### the installed version of Pelican still has the bug.

patched_subclasses = {}
def make_patched_subclass(klass):
    if klass.__name__ not in patched_subclasses:
        class PatchedContent(klass):
            @property
            def url_format(self):
                metadata = super(PatchedContent, self).url_format
                if hasattr(self, 'author'):
                    metadata['author'] = self.author.slug
                if hasattr(self, 'category'):
                    metadata['category'] = self.category.slug

                return metadata
        # Code in core uses Content class names as keys for things.
        PatchedContent.__name__ = klass.__name__
        patched_subclasses[klass.__name__] = PatchedContent
    return patched_subclasses[klass.__name__]

def patch_urlformat(cont):
    # Test whether this content object needs to be patched.
    md = cont.url_format
    if ((hasattr(cont, 'author') and cont.author.slug != md['author']) or
        (hasattr(cont, 'category') and cont.category.slug != md['category'])):
        logger.debug("Detected bug 1547, applying workaround.")
        cont.__class__ = make_patched_subclass(cont.__class__)

### END OF BUG WORKAROUND

def make_category(article, slug):
    '''Make a category object from an index.ext article.

    We add a few attributes to the article object, which
    already contains all the metadata in the index.ext file.
    '''
    # Reuse the article's existing category object.
    category = article.category

    # Setting a category's name resets its slug, so do that first.
    category.name = article.title
    category.slug = slug

    # Description from article text.
    # XXX Relative URLs in the article content may not be handled correctly.
    setattr(category, 'description', article.content)

    # the parent category, defaults to none
    setattr(category, 'parent', None)
    # Children categories (i.e. subcategories). A dict with keys that are
    # subcategory slugs, and values that will be lists of articles.
    setattr(category, 'children', {})
    
    # Metadata, to the extent that this makes sense.
    for k, v in article.metadata.items():
        if k not in ('path', 'slug', 'category', 'name', 'title',
                     'description', 'reader', 'parent', 'children'):
            setattr(category, k, v)

    logger.debug("Category: %s -> %s", category.slug, category.name)
    return category


def pretaxonomy_hook(generator):
    """Use index.ext files to make categories object.

    For a generator, Pelican creates a ``categories`` property, which
    is a list of categories. The elements of that list are also passed
    individually for certain generators (e.g. ``article.html``, 
    ``category.html``) as the ``category`` object.

    Category Metadata adds *subcategories*, where each (sub)category
    is defined by an ``index.ext`` file. Normally, Pelican would see an
    ``index.ext`` file just as another article; in this function, we go
    through the articles, see which ones are ``index.ext`` files, and 
    create category objects, attaching the metadata specified in the
    ``index.ext`` file to those objects. (Note that in fact the object
    already exists; we just expand the functionality.)


    Every *.ext file is an article, as far as Pelican knows. However,
    the index.ext files are actually metadata for a *category*.

    The category *slug* is given by the (sub)directory that the index.ext file
    is in, relative to the root path for articles.

    So, if ``content/articles`` is the root path:

    - content/articles/cat1/index.md
        slug = ``cat1``

    - content/articles/cat1/subcat1/index.md
        slug = ``cat1/subcat1``

    - content/articles/cat1/subcat1/subsubcat1/index.md
        slug = ``cat1/subcat1/subsubcat1``

    And so on.

    .. warning::
        If you are on a Windows system, the category slugs will use the
        backslash: ``cat1\subcat1\subsubcat1``.


    For anything OTHER than ``index.ext`` files, we want to simply treat it
    like a normal article (which we do by placing it in the list 
    ``real_articles``). For ``index.ext`` files, we want, first, to create a
    new category, and then associate the metadata with that category.

    Note that the ``categories`` object in an article context is the
    set of all categories ATTACHED to articles.

    """

    # Start with an empty dict of categories
    category_objects = {}
    # ... and an empty list of articles
    real_articles = []

    # A regex that matches any subdirectory of any of the article paths
    root_paths = re.compile("^(" + re.escape(generator.settings.get('PATH')) +
                    "(?:/|\\\\)(?:" + "|".join(re.escape(artpath)
                            for artpath in generator.settings.get('ARTICLE_PATHS')) +
                    ")(?:/|\\\\))(.*)$")


    # Some articles are regular articles, others define categories
    # We go through all the articles and figure out which is which type 
    for article in generator.articles:
        # Extract the directory and filename (without extension)
        dirname, fname = os.path.split(article.source_path)
        fname, _ = os.path.splitext(fname) # remove extension

        # Remove the root path from each article's dirname
        # and get array of sub-folders; each sub-folder will be a
        # category/subcategory
        m = root_paths.match(dirname)

        # Make sure there is a regex match
        if not m:
            logger.warning("(In category_meta.py, category_meta plugin) - Cannot set category for article! \n" \
                        "Article path does not match pattern for [Article:] %s \n" \
                        " [Source Path:] (%s) \n [Root Paths: ] %s \n [Dirname:] %s",
                             article, article.source_path, root_paths.pattern, dirname)
            cat_slug = os.path.split(dirname)[1] # Set catslug to be directory name
        
        else:
            # Set category slug to be the relative path from root
            # This way, each slug is unique, since you can't have
            # two index.ext files in the same directory
            cat_slug = m.group(2)
        
        # If an index.ext file, we create the category object
        if fname == 'index':
            # Make category and add to category_objects
            category_objects[dirname] = \
                make_category(article, cat_slug)
        
            # If subcategory, make a subcat item in the parent category
            # So, for example, each section is an item (i.e. article) in a chapter
            cat_article = copy.copy(article) # deep copy, so we don't change the article object
            head, tail = os.path.split(cat_slug)
            
            cat_article.slug = tail
            cat_article.source_path, _ = os.path.split(dirname)
            real_articles.append(cat_article)
            
            # If there's a head, then it means it's not a top-level category,
            # so we want an intro slide, unless, of course, .hide_intro_slide is true
            if len(head) > 0 and getattr(article, "hide_intro_slide", False) != "True":
                intro_article = copy.copy(article)
                intro_article.slug = "_" + tail + "0"
                real_articles.append(intro_article)

            
        elif fname[0:1] != "_":
            # For non- index.ext articles, just add them to the real_articles list.
            real_articles.append(article)

    # Attach the dict of categories to the generator object
    setattr(generator, 'all_categories', category_objects)
    
    # Regex to match an article (including index.ext article) to category,
    # based on the location in the file tree.
    # In this regex, we sort category object keys descending by length, 
    # so it matches the deepest folder in the tree
    category_assignment = \
        re.compile("^(" +
                   "|".join(re.escape(prefix)
                            for prefix in 
                                sorted(category_objects.keys(), key=len, reverse=True)) +
                   ")(/|\\\\)?")


    # Attach parent/children categories
    for cat_path, cat in category_objects.items():
        # The category's level is simply the number of nested (sub)directories
        subdir, _ = os.path.split(cat.save_as)
        heirarchy = re.split('(?:/|\\\\)', subdir)
        cat.level = len(heirarchy) - 1

        # If it is not a top-level category, then set the parent category
        # to be the category at the next-higher level, and then add the
        # current category to that parent category's list of children
        if cat.level > 0:
            parentdir, _ = os.path.split(cat_path)
            m = category_assignment.match(parentdir)
            if not m or m.group(1) not in category_objects:
                logger.warn("No parent category for %s (%s)", cat, cat_path)
                # The warning is because it is not level 0, but doesn't have a parent
                # this would happen, e.g., if there was cat/subcat/index.ext but no
                # cat/index.ext -- no index.ext means no category object
            else:
                cat.parent = category_objects[m.group(1)]
                cat.parent.children[cat] = [] # This list will be filled with articles later

    
    # Go through real articles and, based on source path, assign category
    # Later on, Pelican will create the categories object based only on
    # categories that are attached to at least one article.
    for article in real_articles:
        # Use the category_assignment regex to find the article's category
        # based on the source path
        m = category_assignment.match(article.source_path)
        if not m or m.group(1) not in category_objects:
            logger.warning("No category assignment for %s (%s) [%s]",
                         article, article.source_path, m)
            continue
        
        # Attach category object to article
        article.category = category_objects[m.group(1)]
        patch_urlformat(article)

    # Set the generator's articles object to be the list of real articles
    generator.articles = real_articles
    

def register():
    '''Attach the pretaxonomy_hook method to the Pelican signal
    See http://docs.getpelican.com/en/3.6.3/plugins.html#list-of-signals'''
    signals.article_generator_pretaxonomy.connect(pretaxonomy_hook)
