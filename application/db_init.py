# init_db.py

# Intialise the sqlite database

import sqlite3
from sqlite3 import Error
from db_path import DB_PATH

def create_connection(db_file):
    """
    Create a database connection to the SQLite database
    specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """
    Create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    sql_create_elements_table = """ CREATE TABLE IF NOT EXISTS elements (
                                        id integer PRIMARY KEY,
                                        ifc_id integer,
                                        name text NOT NULL,
                                        type text
                                    ); """
    
    sql_create_planes_table = """ CREATE TABLE IF NOT EXISTS planes (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        x float,
                                        y float,
                                        z float
                                    ); """

    # create a database connection
    conn = create_connection(DB_PATH)

    # create tables
    if conn is not None:
        # create elements table
        create_table(conn, sql_create_elements_table)

        # create planes table
        create_table(conn, sql_create_planes_table)

    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
