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
	c.execute("UPDATE Players SET wins = 0;")
	conn.commit()
	c.execute("UPDATE Players SET matches = 0;")
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
	num = c.fetchall()
	num = int(num[0][0])
	conn.commit()
	conn.close()
	return num

def registerPlayer(name):
	'''Register players, it takes one input: the player name'''
	conn = connect()
	c = conn.cursor()
	c.execute("INSERT INTO Players VALUES(%s);",(name,))
	conn.commit()
	conn.close()

def playerStandings():
	'''Returns a list of the players and their win records, sorted by wins.'''
	#This first sql query update the "wins" column. It check how many wins the players have.
	conn = connect()
	c = conn.cursor()
	c.execute("UPDATE Players SET wins = subquery.count FROM (SELECT p.name, p.id, count(*) FROM Matches m, Players p WHERE p.id = m.winner group by p.id) AS subquery WHERE Players.id=subquery.id;")
	conn.commit()
	c.execute("UPDATE Players SET wins = 0 WHERE wins IS NULL;")
	conn.commit()
	conn.close()
	#This second sql query update the "matces" column. It count up how many matches Have the players played.
	conn = connect()
	c = conn.cursor()
	c.execute("UPDATE Players SET matches = subquery.count FROM (SELECT p.name, p.id, count(*) FROM Matches m, Players p WHERE p.id = m.player1 or p.id = m.player2 group by p.id) AS subquery WHERE Players.id=subquery.id;")
	conn.commit()
	c.execute("UPDATE Players SET matches = 0 WHERE matches IS NULL;")
	conn.commit()
	conn.close()
	#This third sql query shows us the the current player standings.
	conn = connect()
	c = conn.cursor()
	c.execute("SELECT id, name, wins, matches FROM Players order by wins desc;")
	standings = c.fetchall()
	conn.commit()
	conn.close()
	return standings
	
def reportMatch(winner, loser):
	'''winner and loser can't be string, these must be integers!'''
	conn = connect()
	c = conn.cursor()
	c.execute("INSERT INTO Matches VALUES(" + str(winner) + ", " + str(loser) + ", " + str(winner) + ", " + str(loser) + ");")
	conn.commit()
	conn.close()
	
def swissPairings():
	'''The number of Players have to be even number.'''
	conn = connect()
	c = conn.cursor()
	c.execute("UPDATE Players SET wins = subquery.count FROM (SELECT p.name, p.id, count(*) FROM Matches m, Players p WHERE p.id = m.winner group by p.id) AS subquery WHERE Players.id=subquery.id;")
	conn.commit()
	c.execute("UPDATE Players SET matches = subquery.count FROM (SELECT p.name, p.id, count(*) FROM Matches m, Players p WHERE p.id = m.player1 or p.id = m.player2 group by p.id) AS subquery WHERE Players.id=subquery.id;")
	conn.commit()
	c.execute("SELECT * FROM Players;")
	result = c.fetchall()
	#pairs is a matrix
	pairs = []
	paired = []
	#pair is a row vector	
	pair = []
	for player1 in result:
		for player2 in result:
			if player1[0] not in paired and player2[0] not in paired and player1[1] != player2[1] and player1[2] == player2[2]:
				pair = [player1[1],player1[0],player2[1],player2[0]]
				paired.append(player1[0])
				paired.append(player2[0])
				pairs.append(pair)
				break
	conn.commit()
	conn.close()
	return pairs