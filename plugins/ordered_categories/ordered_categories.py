'''Copyright 2015, NYU Furman Center

Ordered Categories
******************

A plugin, built on top of the Category Metadata plugin, that allows
for arbitrary ordering of categories. This is useful if, for example,
categories represent sections of a website, and you want to set the
order of the sections on a menu. Or, if you want one category to have
a "next" link going to another.

In the Category Metadata index files, you can add a field with the
sort order (could be numeric or strings, or anything sortable), and
then add a ``CATEGORY_SORT_BY`` setting in the ``pelicanconf.py`` file. The
default is to sort by category slug.

'''
from pelican import signals
import logging

logger = logging.getLogger(__name__)
# Default sort field (can be overridden by config file)
# sort_field = 'slug'


def sorter(el):
    """Sort categories according to ``sort_field``, if set, or else by slug.

    :param el: A tuple of category and list of articles
    """
    cat, articles = el
    if sort_field:
        return getattr(cat, sort_field)
    else:
        return getattr(cat, 'slug')


def create_ordered_categories(generator):
    """For each article/category, set a next and previous sibling.

    """
    # generator.categories is a list of tuples. We want to sort that list
    # based on the attributes of the first element of the tuple (i.e. the
    # category)
    global sort_field  # use global sort field
    # This way, we don't have to go through hoops to pass
    # the sort field to the sorter function
    sort_field = generator.settings['CATEGORY_SORT_BY']
    generator.categories.sort(key=sorter)

    # For each category/articles tuple, if the category has a parent category,
    # attach the list of articles to that parent's children dict
    #
    # If no parent category, then it's a top-level category, so append to the
    # list
    top_level_categories = []
    for i, (cat, articles) in enumerate(generator.categories):
        if cat.parent:
            cat.parent.children[cat].extend(articles)
        else:
            top_level_categories.append([cat, articles])

    def _set_siblings(categories):
        '''Function to set the previous and next sibling category.'''
        for i, (cat, articles) in enumerate(categories):
            setattr(cat, 'prev_sibling', categories[i-1][0] if i > 0 else None)
            setattr(cat, 'next_sibling', categories[i+1][0] if
                    i+1 < len(categories) else None)

            logger.debug("%s -> %s -> %s" % (
                                    getattr(cat.prev_sibling, 'slug', None),
                                    cat.slug,
                                    getattr(cat.next_sibling, 'slug', None)))

    # Go through each category, look for children, and make them siblings
    for i, (cat, articles) in enumerate(generator.categories):
        if cat.children:
            childcats = cat.children.items()
            childcats.sort(key=sorter)
            _set_siblings(childcats)

    # Make siblings for top-level categories
    top_level_categories.sort(key=sorter)
    _set_siblings(top_level_categories)

def register():
    signals.article_generator_finalized.connect(create_ordered_categories)
