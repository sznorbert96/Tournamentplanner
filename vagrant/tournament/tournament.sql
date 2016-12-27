DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;
CREATE TABLE Players(	
	name text
);
ALTER TABLE Players ADD COLUMN id SERIAL PRIMARY KEY;
CREATE TABLE Matches(
	winner	integer references Players(id),
	loser	integer references Players(id)
);
ALTER TABLE Matches ADD COLUMN matchid SERIAL PRIMARY KEY;

--Database created.