CREATE DATABASE tournament;
\c tournament;
CREATE TABLE Players(	
	name text
);
ALTER TABLE Players ADD COLUMN id SERIAL PRIMARY KEY;
ALTER TABLE Players ADD COLUMN wins integer;
ALTER TABLE Players ADD COLUMN matches integer;
CREATE TABLE Matches(
	player1 integer references Players(id),
	player2 integer references Players(id),
	winner	integer references Players(id),
	loser	integer references Players(id)
);
ALTER TABLE Matches ADD COLUMN matchid SERIAL PRIMARY KEY;

--Database created.