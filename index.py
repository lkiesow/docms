#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sqlite3
from mod_python import util


__dir__         = os.path.dirname(__file__)


def index(req):
	req.content_type = 'text/html'
	f = open( os.path.join(__dir__, 'template/index.html'), 'r' )
	body = f.read()
	f.close()

	# check for search parameter
	query = "SELECT * FROM documents ORDER BY title"
	if 'search' in req.form.keys():
		query = "SELECT * FROM documents where title like '%" \
				+ str(req.form['search']) + "%' or tags like '%" \
				+ str(req.form['search']) + "%' ORDER BY title"

	data = ''
	conn = sqlite3.connect(os.path.join(__dir__, 'documents/documents.db'), isolation_level=None)
	cursor = conn.cursor()
	f = open( os.path.join(__dir__, 'template/index.table.html'), 'r' )
	tab = f.read()
	f.close()
	for id, title, creator, subject, description, publisher, \
		contributor, date, type, format, identifier, source, \
		language, relation, coverage, rights, tags, filename \
		in cursor.execute(query):
			
		data += tab % {
					'id':id, 
					'title':title,
					'creator':creator, 
					'subject':subject,
					'publisher':publisher,
					'contributor':contributor,
					'date':date,
					'type':type,
					'format':format,
					'identifier':identifier,
					'source':'<a href="'+source+'">'+source+'</a>',
					'language':language,
					'relation':relation,
					'coverage':coverage,
					'rights':rights,
					'tags':tags,
					'description':description,
					'filename':filename,
					}

	return body % { 'table':data }
