#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from mod_python import util,apache
import uuid
import sqlite3
import shutil

import sys
reload(sys)
sys.setdefaultencoding('utf8')

__dir__         = os.path.dirname(__file__)
read_xmp = apache.import_module(os.path.join(__dir__, 'lib/read_xmp.py'))


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


def __store_file( fileDesc ):
	# Generate UUID
	id = str(uuid.uuid4())
	# Temporary store file in filesystem
	f = open( os.path.join(__dir__, 'tmp/' + id), 'w' )
	f.write( fileDesc.value )
	f.close()
	# Get Dublin Core properties from XMP
	props = read_xmp.get_dc_from_file( os.path.join(__dir__, 'tmp/' + id) )
	# Fill properties with further knowledge
	if not 'format' in props.keys():
		props['format']  = fileDesc.type
	if not 'title' in props.keys():
		props['title']   = fileDesc.filename
	props['id']         = id
	props['filename']   = fileDesc.filename
	props['share_with'] = '[]'
	props['visibility'] = '0'
	read_xmp.fill_dc_prop( props )
	# return prepared HTML
	return props


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
		return inputhtml % { 'inputform' : inputform % __store_file( files ) }
	# got more files
	elif isinstance( files, list ):
		body = ''
		for f in files:
			body += inputform % __store_file( f )
		return inputhtml % { 'inputform':body }
	else:
		util.redirect(req, '..')



def insert(req):
	req.content_type = 'text/plain'
	values = []
	if isinstance( req.form['id'], basestring ):
		id = unicode(req.form['id'])
		if not 'use_' + id in req.form.keys():
			os.remove( os.path.join(__dir__, 'tmp/' + id) )
			util.redirect(req, '..')
		values += [( id,
			unicode(req.form['title']),     unicode(req.form['creator']),
			unicode(req.form['subject']),   unicode(req.form['description']),
			unicode(req.form['publisher']), unicode(req.form['contributor']),
			unicode(req.form['date']),      unicode(req.form['type']), 
			unicode(req.form['format']),    unicode(req.form['identifier']), 
			unicode(req.form['source']),    unicode(req.form['language']),
			unicode(req.form['relation']),  unicode(req.form['coverage']),
			unicode(req.form['rights']),    unicode(req.form['tags']),
			unicode(req.form['filename']) )]
		dest_dir = os.path.join(__dir__, 'documents/' + id + '/')
		os.makedirs(dest_dir)
		shutil.move( os.path.join(__dir__, 'tmp/' + id),
				dest_dir + unicode(req.form['filename']) )
	else:
		for i in range(len(req.form['id'])):
			id = unicode(req.form['id'][i])
			if not 'use_' + id in req.form.keys():
				os.remove( os.path.join(__dir__, 'tmp/' + id) )
				continue
			values += [( id,
				unicode(req.form['title'][i]),     unicode(req.form['creator'][i]),
				unicode(req.form['subject'][i]),   unicode(req.form['description'][i]),
				unicode(req.form['publisher'][i]), unicode(req.form['contributor'][i]),
				unicode(req.form['date'][i]),      unicode(req.form['type'][i]), 
				unicode(req.form['format'][i]),    unicode(req.form['identifier'][i]), 
				unicode(req.form['source'][i]),    unicode(req.form['language'][i]),
				unicode(req.form['relation'][i]),  unicode(req.form['coverage'][i]),
				unicode(req.form['rights'][i]),    unicode(req.form['tags'][i]),
				unicode(req.form['filename'][i]) )]
			dest_dir = os.path.join(__dir__, 'documents/' + id + '/')
			os.makedirs(dest_dir)
			shutil.move( os.path.join(__dir__, 'tmp/' + id ),
					dest_dir + unicode(req.form['filename'][i]) )

	conn = sqlite3.connect(os.path.join(__dir__, 'documents/documents.db'),
			isolation_level=None)
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
