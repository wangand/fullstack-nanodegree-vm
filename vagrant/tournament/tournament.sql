-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- name: Andrew Wang
-- Full Stack Web Developer Nanodegree
-- Project 2 tournament results


-- Create a table called players
-- Has these properties:
-- id - an auto incrementing integer which is the primary key
-- name - a 255 char max varchar, cannot be null
-- wins - the number of matches the player has won
-- matches - the number of matches the player has played
DROP TABLE IF EXISTS players CASCADE;
CREATE TABLE players (
	id SERIAL,
	name VARCHAR(255) NOT NULL,
	wins INT,
	matches INT,
	PRIMARY KEY (id)
);

-- Create a table called matches
-- Has these Properties:
-- id - an auto incrementing integer which is the primary key
-- winner - int corresponding to id of winner
-- loser - int corresponding to id of loser
DROP TABLE IF EXISTS matches;
CREATE TABLE matches(
	id SERIAL,
	winner INT,
	Loser INT,
	FOREIGN KEY(winner) REFERENCES players(id),
	FOREIGN KEY(loser) REFERENCES players(id),
	PRIMARY KEY (id)
);
