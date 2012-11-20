#!/usr/bin/env python
# -*- coding: utf-8 -*-

import libxmp
from libxmp.consts import XMP_NS_DC
from types import NoneType

def __get_dc_array( xmp, dc_prop, name ):
	'''Get a Dublin Core array element from a XMP structure.
	
	Keyword arguments:
	xmp     -- XMP structure (libxmp.core.XMPMeta)
	dc_prop -- a dictionary to store the read properties in
	name    -- name of the element
	'''
	if xmp.does_property_exist(XMP_NS_DC, name):
		dc_prop[name] = []
		for i in range(xmp.count_array_items( XMP_NS_DC, name )):
			dc_prop[name].append( xmp.get_array_item( XMP_NS_DC, name, i+1 ).keys()[0] )


def __get_dc_prop( xmp, dc_prop, name ):
	if xmp.does_property_exist(XMP_NS_DC, name):
		dc_prop[name] = xmp.get_property(XMP_NS_DC, name)


def __get_dc_lang_prop( xmp, dc_prop, name, lang_specific, lang_generic=None ):
	if xmp.does_property_exist(XMP_NS_DC, name):
		dc_prop[name] = xmp.get_localized_text( XMP_NS_DC, name, 
				lang_generic, lang_specific)


def __get_dc( xmp ):
	dc_prop = {}
	__get_dc_array(     xmp, dc_prop, 'contributor' )
	__get_dc_prop(      xmp, dc_prop, 'coverage' )
	__get_dc_array(     xmp, dc_prop, 'creator' )
	__get_dc_array(     xmp, dc_prop, 'date' )
	__get_dc_lang_prop( xmp, dc_prop, 'decsription', 'en-us', 'en' )
	__get_dc_prop(      xmp, dc_prop, 'format' )
	__get_dc_prop(      xmp, dc_prop, 'identifier' )
	__get_dc_array(     xmp, dc_prop, 'language' )
	__get_dc_array(     xmp, dc_prop, 'publisher' )
	__get_dc_array(     xmp, dc_prop, 'relation' )
	__get_dc_lang_prop( xmp, dc_prop, 'rights', 'en-us', 'en' )
	__get_dc_array(     xmp, dc_prop, 'source' )
	__get_dc_prop(      xmp, dc_prop, 'subject' )
	__get_dc_lang_prop( xmp, dc_prop, 'title', 'en-us', 'en' )
	__get_dc_array(     xmp, dc_prop, 'type' )
	return dc_prop


def get_dc_from_file( filename ):
	'''Get an embedded XMP from a media file (PDF, JPEG, …) and extract the
	Dublin Core elements.
	
	Keyword arguments:
	filename -- name of the media file
	'''
	xmpfile = libxmp.XMPFiles( file_path=filename )
	xmp = xmpfile.get_xmp()
	return {} if type(xmp) is NoneType else __get_dc(xmp)


def get_dc_from_xmp( filename ):
	'''Load XMP from a file and extract the Dublin Core elements.
	
	Keyword arguments:
	filename -- name of the XMP file
	'''
	f = open(filename, 'r')
	xmpstr = f.read()
	f.close()
	xmp = libxmp.core.XMPMeta( xmp_str=xmpstr )
	return {} if type(xmp) is NoneType else __get_dc(xmp)


def fill_dc_prop( dc_prop, fill='' ):
	'''Fill a dictionary in such a way that all Dublin Core elements exists. If
	they did not exist before, their value is set to 'fill'.
	
	Keyword arguments:
	dc_prop -- a dictionary to store the properties in
	fill    -- Text to fill the elements with (default '')
	'''
	dc_elem = ['contributor', 'coverage', 'creator', 'date', 'decsription',
			'format', 'identifier', 'language', 'publisher', 'relation', 'rights',
			'source', 'subject', 'title', 'type']
	for e in dc_elem:
		if not e in dc_prop.keys():
			dc_prop[e] = fill
	return dc_prop
