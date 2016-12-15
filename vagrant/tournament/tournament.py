#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    '''It delete all the registered matches from Matches table'''
	conn = connect()
	c = conn.cursor()
	c.execute("DELETE FROM Matches;")
	conn.commit()
	conn.close()



def deletePlayers():
    '''This procedure deletes all the registered players from the Players table (takes no input).'''
	conn = connect()
	c = conn.cursor()
	c.execute("DELETE FROM Players;")
	conn.commit()
	conn.close()

def countPlayers():
    '''Returns a single number, which gives the number of the registered players in the tournament'''
	conn = connect()
	c = conn.cursor()
	c.execute("SELECT count(id) as num FROM Players;")
	conn.commit()
	conn.close()

def registerPlayer(name):
    '''Register players, it takes one input: the player name'''
	conn = connect()
	c = conn.cursor()
	c.execute("INSERT INTO Players VALUES('" + str(name) + "');")
	conn.commit()
	conn.close()

def playerStandings():
    '''Returns a list of the players and their win records, sorted by wins.'''
    #This first sql query update the "wins" column. It check how many wins the players have.
    conn = connect()
    c = conn.cursor()
    c.execute("UPDATE Players SET wins = subquery.count FROM (SELECT p.name, p.id, count(*) FROM Matches m, Players p WHERE p.id = m.winner group by p.id) AS subquery WHERE Players.id=subquery.id;")
    conn.commit()
    conn.close()
    #This second sql query update the "matces" column. It count up how many matches Have the players played.
    conn = connect()
    c = conn.cursor()
    c.execute("UPDATE Players SET matches = subquery.count FROM (SELECT p.name, p.id, count(*) FROM Matches m, Players p WHERE p.id = m.player1 or p.id = m.player2 group by p.id) AS subquery WHERE Players.id=subquery.id;")
    conn.commit()
    conn.close()
    #This third sql query shows us the the current player standings.
    conn = connect()
	c = conn.cursor()
	c.execute("SELECT id, name, wins, matches FROM Players order by won desc;")
	conn.commit()
	conn.close()


def reportMatch(winner, loser):
    '''winner and loser can't be string, these must be integers!'''
	conn = connect()
	c = conn.cursor()
	c.execute("INSERT INTO Matches VALUES(" + str(winner) + ", " + str(loser) + ", " + str(winner) + ", " + str(loser) + ");")
	conn.commit()
	conn.close()

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
