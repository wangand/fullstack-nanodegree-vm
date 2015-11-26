Name: Andrew Wang
Full Stack Web Developer Nanodegree
Project 2 tournament results

README file

Setting up the tournament database:
1. Navigate to the tournament file in vagrant
2. Create the tournament database in psql: 
	psql tournament
3. In the psql command line import tournament.sql:
	\i tournament.sql
4. Exit psql:
	\q

Running the tests:
1. Make sure you are in the tournament file in vagrant
2. Use python to run tournament_test.py:
	python tournament_test.py