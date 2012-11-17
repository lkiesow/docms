#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from mod_python import util
import uuid
import sqlite3
import shutil


__dir__         = os.path.dirname(__file__)


def upload(req, files):
	req.content_type = 'text/html'

	# Read template
	f = open( os.path.join(__dir__, 'template/input.form.html'), 'r' )
	inputform = f.read()
	f.close()
	f = open( os.path.join(__dir__, 'template/input.html'), 'r' )
	inputhtml = f.read()
	f.close()

	# got one file
	if isinstance( files, util.Field ):
		id = str(uuid.uuid4())
		f = open( os.path.join(__dir__, 'tmp/' + id), 'w' )
		f.write( files.value )
		f.close()
		x = inputform % { 'id':id, 'filename':files.filename, 'format':files.type }
		return inputhtml % { 'inputform':x }

	# got more files
	elif isinstance( files, list ):
		body = ''
		for f in files:
			id = str(uuid.uuid4())
			fi = open( os.path.join(__dir__, 'tmp/' + id), 'w' )
			fi.write( f.value )
			fi.close()
			body += inputform % { 'id':id, 'filename':f.filename, 'format':f.type }
		return inputhtml % { 'inputform':body }
	else:
		util.redirect(req, '..')


def insert(req):
	req.content_type = 'text/plain'
	values = []
	if isinstance( req.form['id'], basestring ):
		id = str(req.form['id'])
		values += [( id,
			str(req.form['title']),     str(req.form['creator']),
			str(req.form['subject']),   str(req.form['description']),
			str(req.form['publisher']), str(req.form['contributor']),
			str(req.form['date']),      str(req.form['type']), 
			str(req.form['format']),    str(req.form['identifier']), 
			str(req.form['source']),    str(req.form['language']),
			str(req.form['relation']),  str(req.form['coverage']),
			str(req.form['rights']),    str(req.form['tags']),
			str(req.form['filename']) )]
		os.makedirs(os.path.join(__dir__, 'documents/' + id))
		shutil.move( os.path.join(__dir__, 'tmp/' + id),
				os.path.join(__dir__, 'documents/' + id + '/' 
					+ str(req.form['filename']) ))
	else:
		for i in range(len(req.form['id'])):
			values += [(                      str(req.form['id'][i]),
				str(req.form['title'][i]),     str(req.form['creator'][i]),
				str(req.form['subject'][i]),   str(req.form['description'][i]),
				str(req.form['publisher'][i]), str(req.form['contributor'][i]),
				str(req.form['date'][i]),      str(req.form['type'][i]), 
				str(req.form['format'][i]),    str(req.form['identifier'][i]), 
				str(req.form['source'][i]),    str(req.form['language'][i]),
				str(req.form['relation'][i]),  str(req.form['coverage'][i]),
				str(req.form['rights'][i]),    str(req.form['tags'][i]),
				str(req.form['filename'][i]) )]
			os.makedirs(os.path.join(__dir__, 'documents/' + str(req.form['id'][i])))
			shutil.move( os.path.join(__dir__, 'tmp/' + str(req.form['id'][i])),
					os.path.join(__dir__, 'documents/' + str(req.form['id'][i]) + '/' + str(req.form['filename'][i]) ))

	conn = sqlite3.connect(os.path.join(__dir__, 'documents/documents.db'), isolation_level=None)
	cursor = conn.cursor()
	cursor.executemany(u'''insert into documents (
			id, title, creator, subject, description, publisher, contributor,
			date, type, format, identifier, source, language, relation, coverage,
			rights, tags, filename) 
			values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', values )
	conn.commit()
	util.redirect(req, '..')


def index(req):
	req.content_type = 'text/html'
	f = open( os.path.join(__dir__, 'template/uploadform.html'), 'r' )
	body = f.read()
	f.close()
	return body
