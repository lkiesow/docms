#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sqlite3
from mod_python import util

import sys
reload(sys)
sys.setdefaultencoding('utf8')


__dir__ = os.path.dirname(__file__)


def index(req, id):
	req.content_type = 'text/plain'

	query = "select filename, format from documents where id='%s'" % id
	conn = sqlite3.connect(
			os.path.join(__dir__, 'documents/documents.db'), 
			isolation_level=None)
	cursor = conn.cursor()
	for filename, format in cursor.execute(query):
		f = open( os.path.join(__dir__, 'documents/' + id + '/' + filename ), 'r' )
		body = f.read()
		f.close()
		req.content_type = str(format)
		req.headers_out['Content-Disposition'] = 'attachment; filename=' + str(filename)
		return body
	util.redirect(req, '..')
