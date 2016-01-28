# Project 3 Catalog


## Installation
Database and application are already set up in the /vagrant/catalog directory. To refresh schema and add some items:

1. Make sure you are in the /vagrant/catalog directory
2. Use refreshschema.py to refresh schema:
    ```
    python refreschschema.py
    ```
3. Use additems.py to add some items:
    ```
    python additems.py
    ```

## Usage

Activate application.py and use a web browser to access localhost:8000

1. Make sure you are in the /vagrant/catalog directory
2. Run application.py with python
    ```
    python application.py
    ```
3. Open localhost:8000 in a web browser. Be sure to use localhost:8000. Other addresses such as 127.0.0.1 will not work
    ```
    http://localhost:8000/
    ```
4. View the catalog without logging in or login with Google to add, edit, and delete items created by you.

## Limitations
* Each item name in this catalog is unique since it is confusing to have two items with the exact same name.
    * If you would like to add a similar item, make the name different (e.g. brush2)