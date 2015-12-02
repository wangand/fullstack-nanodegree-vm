-- Create the flaskr database
DROP DATABASE IF EXISTS flaskr;
CREATE DATABASE flaskr;

-- Create entries table
DROP TABLE IF EXISTS entries;
CREATE TABLE entries(
	id SERIAL,
	title TEXT,
	text TEXT,
	PRIMARY KEY (id)
);

SELECT * FROM entries;

INSERT INTO entries (title, text) VALUES ('CAT', 'MEOW');
SELECT * FROM entries;