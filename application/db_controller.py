# db_controller.py

# Controller class to perform CRUD operations on sqlite database

import sqlite3
from sqlite3 import Error


class DBController:
    """
    A controller for the SQLite table which facilitates
    CRUD operations.
    """
    def __init__(self, database):
        self.database = database
        self.conn = self._create_connection()
    
    def _create_connection(self):
        """
        Create a database connection to the SQLite database
        specified by self.database
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(self.database)
            return conn
        except Error as e:
            print(e)

        return conn

    def create(self, item):
        """
        Create a new element into the elements table
        :param item:
        :return: item id
        """
        with self.conn:  # type: ignore
            sql = ''' INSERT INTO elements(ifc_id,name,type)
                    VALUES(?,?,?) '''
            cur = self.conn.cursor()  # type: ignore
            cur.execute(sql, item)
            self.conn.commit()  # type: ignore
        return cur.lastrowid
    
    def update(self, item):
        """
        Update priority, begin_date, and end date of a item
        :param item:
        :return: item id
        """
        with self.conn:  # type: ignore
            sql = ''' UPDATE elements
                    SET ifc_id = ? ,
                        name = ? ,
                        type = ?
                    WHERE id = ?'''
            cur = self.conn.cursor()  # type: ignore
            cur.execute(sql, item)
            self.conn.commit()  # type: ignore

    def delete(self, item_id):
        """
        Delete a item by item id
        :param conn:  Connection to the SQLite database
        :param id: id of the item
        :return:
        """
        with self.conn:  # type: ignore
            sql = 'DELETE FROM elements WHERE id=?'
            cur = self.conn.cursor()  # type: ignore
            cur.execute(sql, (item_id,))
            self.conn.commit()  # type: ignore

    def delete_all(self):
        """
        Delete all rows in the table
        :param conn: Connection to the SQLite database
        :return:
        """
        with self.conn:  # type: ignore
            sql = 'DELETE FROM elements'
            cur = self.conn.cursor()  # type: ignore
            cur.execute(sql)
            self.conn.commit()  # type: ignore
