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

cursor.execute('''CREATE TABLE user
					( username text primary key, 
					passwd text, salt text )''')

conn.commit()
