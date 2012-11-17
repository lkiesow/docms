import sqlite3
 
conn = sqlite3.connect('documents.db')
 
cursor = conn.cursor()
 
# create a table
cursor.execute('''CREATE TABLE documents
					( id text primary key, 
					title text, creator text, subject text,
					description text, publisher text, contributor text, date text,
					type text, format text, identifier text, source text, 
					language text, relation text, coverage text, rights text,
					tags text, filename text ) ''')

# cursor.execute('''insert into documents (title, creator, subject, description, publisher, contributor, date, type, format, identifier, source, language, relation, coverage, rights, tags, filename) values ( 'XMP Specification - Part 1, Data model, Serialization, and Core Properties', 'Adobe Systems', 'metadata. XMP, specification', 'Covers the basic metadata representation model that is the foundation of the XMP standard format. The Data Model prescribes how XMP metadata can be organized; it is independent of file format or specific usage. The Serialization Model prescribes how the Data Model is represented in XML, specifically RDF.', "Adobe Systems", '', '2012-04', 'medium', 'application/pdf', 'XMPSpec1', 'http://www.adobe.com/devnet/xmp.html', 'en', '', '', '', 'xmp, specs, specification, metadata', 'XMPSpecificationPart1.pdf' )''' )

conn.commit()
