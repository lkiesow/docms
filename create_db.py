import sqlite3
 
### Connect to the database
conn = sqlite3.connect('documents/documents.db')
cursor = conn.cursor()
 
### Create document table
# * ID is short for the Dublin Core identifier
# * filename, share_with, user and visibility are additional properties not
#   included in the Dublin Core element set but we need them :-)
#    - filename defines the filename and thus the location of the element
#    - user defines the user to whom the document belongs to
#    - share_with defines a list of users which can access to the document
#    - visibility defines if the document can be seen by the owner alone (0),
#      or additionally by the users in share_with (1), or by all users (2), or
#      by all users and nonusers (3).
cursor.execute('''CREATE TABLE documents
					( 
						id text primary key, 

						contributor text, 
						coverage text, 
						creator text, 
						date text,
						description text, 
						format text, 
						language text, 
						publisher text, 
						relation text, 
						rights text,
						source text, 
						subject text,
						title text, 
						type text, 

						filename text,
						share_with text,
						user text,
						visibility integer
					) ''')

### Create user table
# * username: Should contain only [a-z0-9_-]
# * realname: The real name of the user
# * password: sha256 hash of password + salt
# * salt:     Random string for salting the hashed password
# * status:   user (0), admin (1)
cursor.execute('''CREATE TABLE user
					(
						username text primary key, 
						realname text,
						passwd   text, 
						salt     text,
						status   integer
					)''')

### Create default user
#   username: admin
#   password: admin
import random
random.seed()
salt = random.randrange(0,1000000000000)
import hashlib
sha  = hashlib.sha256()
sha.update('admin' + str(salt))
query = '''insert into user (
		username, 
		realname, 
		passwd, 
		salt, 
		status
	) values (
		'admin',
		'Administrator',
		'%(passwd)s',
		'%(salt)s',
		1
	)''' % {
			'passwd' : sha.hexdigest(),
			'salt'   : salt
	}
cursor.execute(query)

conn.commit()
