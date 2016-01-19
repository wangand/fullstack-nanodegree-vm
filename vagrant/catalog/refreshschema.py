import sqlite3


"""
This script refreshes the schema of the catalog database
Author: Andrew Wang
"""

conn.close()
conn = sqlite3.connect('catalog.db')
c = conn.cursor()
c.execute('drop table if exists items')
c.execute('drop table if exists users')
c.execute('drop table if exists categories')
conn.commit()
