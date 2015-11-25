#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#
# name: Andrew Wang
# Full Stack Web Developer Nanodegree
# Project 2 tournament results

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("DELETE FROM matches")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("DELETE FROM players")
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("SELECT COUNT (id) FROM players")
    result = cursor.fetchone()
    DB.close()
    return result[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("INSERT INTO players (name, wins, matches) "
        "VALUES (%s, %s, %s)", (name,0,0))
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("SELECT id, name, wins, matches "
        "FROM players ORDER BY wins DESC")
    results = cursor.fetchall()
    DB.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    cursor = DB.cursor()
    # Add match
    cursor.execute("INSERT INTO matches (winner, loser) "
        "VALUES (%s, %s)", (winner, loser))
    # Update winner
    cursor.execute("UPDATE players "
        "SET wins = wins+1, matches = matches+1"
        "WHERE id = %s", (winner,))
    # Update loser
    cursor.execute("UPDATE players "
        "SET matches = matches+1"
        "WHERE id = %s", (loser,))
    # Commit all changes and close connection
    DB. commit()
    DB.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    # Get standings
    standings = playerStandings()
    retval = []
    # Open connection
    DB = connect()
    cursor = DB.cursor()
    # Add standings 2 by 2 in order to returned list
    for i in range(0,len(standings),2):
        tempId1 = standings[i][0]
        tempName1 = standings[i][1]
        tempId2 = standings[i+1][0]
        tempName2 = standings[i+1][1]
        retval.append((tempId1, tempName1, tempId2, tempName2))
    DB.close()
    return retval

