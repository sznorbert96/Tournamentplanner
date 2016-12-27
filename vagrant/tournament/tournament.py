import psycopg2


def connect():
	'''Connect to the PostgreSQL database. Returns a database connection.'''
	return psycopg2.connect("dbname=tournament")


def deleteMatches():
	'''It delete all the registered matches from Matches table'''
	conn = connect()
	c = conn.cursor()
	c.execute("TRUNCATE Matches CASCADE;")
	conn.commit()
	conn.close()


def deletePlayers():
	'''This procedure deletes all the registered players from the Players table (takes no input).'''
	conn = connect()
	c = conn.cursor()
	c.execute("TRUNCATE Players CASCADE;")
	conn.commit()
	conn.close()


def countPlayers():
	'''Returns a single number, which gives the number of the registered players in the tournament'''
	conn = connect()
	c = conn.cursor()
	c.execute("SELECT count(id) as num FROM Players;")
	num = c.fetchall()
	# we convert the num to integer.
	num = int(num[0][0])
	conn.commit()
	conn.close()
	return num


def registerPlayer(name):
	'''Register players, it takes one input: the player name'''
	conn = connect()
	c = conn.cursor()
	c.execute("INSERT INTO Players VALUES(%s);", (name,))
	conn.commit()
	conn.close()

	
def playerStandings():
	'''Returns a list of the players and their win records, sorted by wins.'''
	standings = []
	standings_losers = []
	conn = connect()
	c = conn.cursor()
	# This first sql query check for the winners,
	# we store it in "winners".
	c.execute("SELECT p.id, p.name, wins.count as wins, matches.count as "
	"matches FROM Players AS p, (SELECT p.name, p.id, count(*) FROM "
	"Matches m, Players p WHERE p.id = m.winner group by p.id order by "
	"p.id) AS wins, (SELECT p.id, p.name, count(*) FROM Matches m, "
	"Players p WHERE p.id = m.winner or p.id = m.loser group by p.id) "
	"AS matches WHERE p.id = wins.id and p.id = matches.id order by wins.count desc;")
	winners = c.fetchall()
	conn.commit()
	conn.close()
	conn = connect()
	c = conn.cursor()
	# This query gives us how many matches have the players played,
	# then we store this data in a "result" variable.
	c.execute("SELECT p.id, p.name, subquery.count as matches FROM "
	"(SELECT p.name, p.id, count(*) FROM Matches m, Players p WHERE "
	"p.id= m.winner or p.id = m.loser group by p.id) AS subquery, "
	"Players as p WHERE p.id=subquery.id;")
	result = c.fetchall()
	conn.commit()
	# At this if statement we make sure "result" is not empty which means,
	# the players did play matches, if result is empty
	# then we return zero matches and zero wins for every players.
	if result == []:
		c.execute("SELECT p.id, p.name, 0, 0 FROM Players as p;")
		result = c.fetchall()
		conn.commit()
		conn.close()
		return result
	# At this query we set the wins equal to zero
	# and count the matches that each player has played.
	c.execute("SELECT p.id, p.name, 0 as wins, subquery.count as matches FROM (SELECT p.name, p.id, count(*) FROM Matches m, Players p WHERE p.id = m.winner or p.id = m.loser group by p.id) AS subquery, Players as p WHERE p.id=subquery.id;")
	result = c.fetchall()
	conn.commit()	
	# If winners is empty then we don't have to worry about wins
	# what we set before at line 73 is fine for that case.
	if winners != []:
		if len(winners) <= 1:
			for row in result:
				if row[0] == winners[0][0]:
					# We walk through the "result" list/tuple and we want to find where,
					# row[0] which is Player id matches winner[0][0] which is again a Player id
					# in this case we assuming that, the winners list only has one row.
					# If the line 80 is true, then we set the "row" vector second and third element,
					# equal to the winners second and third element , before that we have to convert
					# the tuple to a list.
					lst_row = list(row)
					lst_row[2] = int(winners[0][2])
					lst_row[3] = int(winners[0][3])
					row = tuple(lst_row)
					standings.append(row)
				else:
					# If the line 80 is not true we only convert the row second and third element to an int,
					# then we append these "row"s to the "standings_losers" list.
					lst_row = list(row)
					lst_row[2] = int(lst_row[2])
					lst_row[3] = int(lst_row[3])
					row = tuple(lst_row)
					standings_losers.append(row)
				
		else:
			# line 78 is not true, the program this part will run. When "winners" length is bigger than 1.
			# if winners is bigger than 1 , it means we have to iterate through this winners tuple to check
			# is players id(row[0]) in the winners list. We have to use here two for loop.
			for row in result:
				not_in = True
				# We have to care about when row[0] != winner[0]
				# if we just make an else statement for that then we will have a duplicated "standings_losers" tuple,
				# so I used a bool  variable.
				for winner in winners:
					if row[0] == winner[0]:
						lst_row = list(row)
						lst_row[2] = int(winner[2])
						lst_row[3] = int(winner[3])
						row = tuple(lst_row)
						standings.append(row)
						not_in = False
				if not_in == True:
					# We check for this statement at the end, if not_in is still True,
					# it means that the Player wasn't in the "winner" tuple.
					lst_row = list(row)
					lst_row[2] = int(lst_row[2])
					lst_row[3] = int(lst_row[3])
					row = tuple(lst_row)
					standings_losers.append(row)
	conn.close()
	standings_losers = sorted(standings_losers)
	# We sort the standings_losers by 
	# the first column which is the Players ID.
	# We don't have to sort the standings,
	# because we sorted it in the sql query by wins desc.
	# Then we add up the two tuple and return it.
	return standings+standings_losers

	
def reportMatch(winner, loser):
	'''winner and loser can't be string, these must be integers!'''
	conn = connect()
	c = conn.cursor()
	c.execute("INSERT INTO Matches VALUES(%s, %s);" , (winner, loser,))
	conn.commit()
	conn.close()
	playerStandings()

	
def swissPairings():
	'''The number of Players have to be even number.'''
	# we set result equal to playerStandings()
	# this variable will hold the actual standings.
	result = playerStandings()
	# pairs is a matrix
	pairs = []
	count = 0
	while count < (len(result)):
		pairs.append((result[count][0], result[count][1], result[count+1][0], result[count+1][1]))
		count += 2
	return pairs