-- name: Andrew Wang
-- Full Stack Web Developer Nanodegree
-- Project 3 Catalog

-- Create the tournament database
DROP DATABASE IF EXISTS catalog;
CREATE DATABASE catalog;

-- Create a table called users
-- Has these properties:
-- id - an auto incrementing integer which is the primary key
-- user_name - a 255 char max varchar, the user's user name
-- hash - a hash of the user's password
-- salt - the salt of the user's password
DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users (
	id SERIAL,
	user_name VARCHAR(255) NOT NULL,
	hash TEXT NOT NULL,
	salt TEXT NOT NULL,
	PRIMARY KEY (id)
);

-- Create a table called items
-- Has these Properties:
-- id - an auto incrementing integer which is the primary key
-- creator - int corresponding to id of item creator in users
-- name - a 255 char max varchar, name of item
-- catagory - a 255 char max varchar, category of item
DROP TABLE IF EXISTS items;
CREATE TABLE items(
	id SERIAL,
	creator INT NOT NULL,
	name VARCHAR(255),
	category VARCHAR(255),
	FOREIGN KEY(creator) REFERENCES users(id),
	PRIMARY KEY (id)
);

SELECT * FROM users;
SELECT * FROM items;
