#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sqlite3
from mod_python import util

import sys
reload(sys)
sys.setdefaultencoding('utf8')

__dir__         = os.path.dirname(__file__)


def modify(req):
	req.content_type = 'text/plain'
	values = []
	id = unicode(req.form['id'])
	values += [(
		unicode(req.form['title']),     unicode(req.form['creator']),
		unicode(req.form['subject']),   unicode(req.form['description']),
		unicode(req.form['publisher']), unicode(req.form['contributor']),
		unicode(req.form['date']),      unicode(req.form['type']), 
		unicode(req.form['format']),    unicode(req.form['identifier']), 
		unicode(req.form['source']),    unicode(req.form['language']),
		unicode(req.form['relation']),  unicode(req.form['coverage']),
		unicode(req.form['rights']),    unicode(req.form['tags']),
		unicode(req.form['filename']),  id )]

	conn = sqlite3.connect(os.path.join(__dir__, 'documents/documents.db'), isolation_level=None)
	cursor = conn.cursor()
	cursor.executemany(u'''update documents set
			title=?, creator=?, subject=?, description=?, publisher=?, contributor=?,
			date=?, type=?, format=?, identifier=?, source=?, language=?, relation=?, coverage=?,
			rights=?, tags=?, filename=? where id=?''', values )
	conn.commit()
	util.redirect(req, '..')


def index(req, id):
	req.content_type = 'text/html'
	f = open( os.path.join(__dir__, 'template/modify.html'), 'r' )
	body = f.read()
	f.close()

	query = "SELECT * FROM documents where id = ?"

	conn = sqlite3.connect(os.path.join(__dir__, 'documents/documents.db'), isolation_level=None)
	cursor = conn.cursor()
	for id, title, creator, subject, description, publisher, \
		contributor, date, type, format, identifier, source, \
		language, relation, coverage, rights, tags, filename \
		in cursor.execute(query, [(id)]):
			
		body = body % {
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
					'source':source,
					'language':language,
					'relation':relation,
					'coverage':coverage,
					'rights':rights,
					'tags':tags,
					'description':description,
					'filename':filename,
					}

	return body
