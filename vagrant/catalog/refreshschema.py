# name: Andrew Wang
# Full Stack Web Developer Nanodegree
# Project 3 Catalog


import sqlite3
import database_setup


"""
This script refreshes the schema of the catalog database
Author: Andrew Wang
"""


# Delete Schema
conn = sqlite3.connect('catalog.db')
c = conn.cursor()
c.execute('drop table if exists items')
c.execute('drop table if exists users')
c.execute('drop table if exists categories')
conn.commit()
conn.close()
