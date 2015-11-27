# Project 2 Tournament Results

## Installation

Setting up the tournament database:

1. Navigate to the tournament file in vagrant
2. Create the tournament database in psql:
    ``` 
    psql tournament
    ```
3. In the psql command line import tournament.sql:
    ```
    \i tournament.sql
    ```
4. Exit psql:
    ```
    \q
    ```

## Usage

Running the tests:

1. Make sure you are in the tournament file in vagrant
2. Use python to run tournament_test.py from the command line:
    ```
    python tournament_test.py
    ```

## Limitations

* This tournament result system only handles tournaments
that have an even number of participants.
* This tournament result system cannot handle draws