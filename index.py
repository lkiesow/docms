#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sqlite3
from mod_python import util

import sys
reload(sys)
sys.setdefaultencoding('utf8')

__dir__         = os.path.dirname(__file__)

__auth_realm__ = "Members only"

def __auth__(req, user, passwd):
	query = "select passwd, salt from user where username='%s'" % user
	conn = sqlite3.connect(
			os.path.join(__dir__, 'documents/documents.db'), 
			isolation_level=None)
	cursor = conn.cursor()
	for hashedpasswd, salt in cursor.execute(query):
		import hashlib
		sha = hashlib.sha256()
		sha.update(passwd+salt)
		if hashedpasswd == sha.hexdigest():
			return 1
	return 0


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
	conn = sqlite3.connect(os.path.join(__dir__, 'documents/documents.db'),
			isolation_level=None)
	cursor = conn.cursor()
	f = open( os.path.join(__dir__, 'template/index.table.html'), 'r' )
	tab = unicode(f.read()).decode('utf-8')
	f.close()
	for id, contributor, coverage, creator, date, description, format, \
			language, publisher, relation, rights, source, subject, title, type, \
			filename, share_with, user, visibility \
		in cursor.execute(query):
			
		data += tab.decode('utf-8') % {
					'id':id, 

					'contributor':contributor,
					'coverage':coverage,
					'creator':creator, 
					'date':date,
					'description':description,
					'format':format,
					'language':language,
					'publisher':publisher,
					'relation':relation,
					'rights':rights,
					'source':'<a href="'+source+'">'+source+'</a>',
					'subject':subject,
					'title':title,
					'type':type,

					'filename':filename,
					'share_with':share_with,
					'visibility':visibility,
					}

	return body % { 'table':data }
