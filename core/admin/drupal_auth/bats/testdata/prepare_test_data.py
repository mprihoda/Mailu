import sqlite3

conn = sqlite3.connect("testdata.sqlite")
conn.executescript('''
DROP TABLE IF EXISTS users;
CREATE TABLE users (name VARCHAR(255) NOT NULL PRIMARY KEY, pass VARCHAR(255));
INSERT INTO users VALUES ('testuser', '$S$D4rHeM6Yb3Pqvr.3unYTA1xEOPazIsaIG5NdYOV..yN0UNC59TAz'); -- testpwd
INSERT INTO users VALUES ('anotheruser', '$S$DD7BWIOu2YDNWRJ7wcGFdUN2DbuBunEN56EaqCHXRY7d3Ccu.Ucd'); -- admin123
''')
conn.close()