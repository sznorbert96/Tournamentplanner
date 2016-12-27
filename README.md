# Tournamentplanner

## Synopsis

This program is a tournament planner, which manages Players and matches. With this program you can organize a tournament ,but the number of the players has to be even. This program uses SQL database, it stores datas about players, and about the matches. 

## Code Explonation

If you want to use this program:

1. First of all you have to import everything from tournament.py ( "from tournament import *")
2. You have to register Players to the database. The number of players have to be even. (registerPlayer(name), example: registerPlayer("John Stevens") ==> John Stevens registered to the database, in the Players table.
3. You may want to chech if there are even number of Players. For this use "countPlayers()". It will return a single number, which is the number of registered Players.
4. You have to pair up the Players with the "swissPairings()" procedure. It will provide a tuple with the pairs where Players ids, and names appear (example: John Stevens vs Bob Sinclar will looks like this: (1, John Stevens, 2, Bob Sinclar))
5. You have to report the result of the match with the "reportMatch(winner, loser)" procedure.
Where winner means the id of the winner and loser means the id of the loser player.
(example: if John Stevens was the winner you have to report like this : reportMatch(1,2))
6. You can check for the player standings with the "playerStandings()" procedure.
7. Then you can pair up the players again until you got a tournament winner.

You can reset your database with these procedures:

deleteMatches() ==> it deletes all the matches from the Matches table.

deletePlayers() ==> it deletes all the Players from the Players table.
