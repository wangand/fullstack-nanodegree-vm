#
# Database access functions for the web forum.
# 

import time
import psycopg2
import bleach

## Database connection
DB = []

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    connection1 = psycopg2.connect("dbname=forum")
    cursor = connection1.cursor()
    cursor.execute("SELECT * FROM posts")
    DB = cursor.fetchall()
    posts = [{'content': str(row[1]), 'time': str(row[0])} for row in DB]
    posts.sort(key=lambda row: row['time'], reverse=True)
    connection1.close()
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    content = bleach.clean(content)
    connection1 = psycopg2.connect("dbname=forum")
    cursor = connection1.cursor()
    #t = time.strftime('%c', time.localtime())
    cursor.execute("INSERT INTO posts (content) VALUES (%s)", (content,))
    connection1.commit()
    connection1.close()
