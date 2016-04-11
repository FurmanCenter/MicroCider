
from pelican import signals
import pprint
import os
import logging
from table_fu import TableFu
import pdb
logger = logging.getLogger(__name__)


def data_import(generator, content=None):
	if not content:
		# Then it's a page, not an article
		#pdb.set_trace()
		contents = getattr(generator, 'pages')
	else:
		# An article, so content is only one element
		# To make it work with pages (where content is an array)
		# we need to create an array
		contents = [content]

	for content_obj in contents:
		if hasattr(content_obj, 'data') and len(content_obj.data) > 0:
			# if isinstance(content.data, (str, basestring)): # make string into 1-item list
			# 	data = [content.data]
			# else:
			# 	data = content.data
			data = content_obj.data.split('|')
			#print data
			datatables = []
			for d in data:
				logger.debug("Loading data <%s> for article %s" % (d, content_obj.slug))
				#logger.debug(os.getcwd())
				#pdb.set_trace()
				filepath = os.path.join(os.getcwd(), generator.settings['PATH'], generator.settings['DATA_PATH'], d)
				
				try:
					_data = TableFu.from_file(filepath)
					datatables.append(_data)
					#setattr(content, 'datatable', data)
				except:
					#raise
					logger.warn("Could not load data file for %s: %s" % (content_obj.slug, filepath))
				setattr(content_obj, 'datatables', datatables)

		elif hasattr(content_obj, 'mapdata') and len(content_obj.mapdata) > 0:
			# If mapdata but no data, add empty datatables object so that
			# figure titles and captions will work
			datatable = { 'rows': [], 'columns': [] }
			setattr(content_obj, 'datatables', [datatable])

def register():
    signals.article_generator_write_article.connect(data_import)
    signals.page_generator_finalized.connect(data_import)