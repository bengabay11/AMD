import sqlite3


class DataBase:
    """The class is incharge of saving data in the database."""
    def __init__(self):
        """The function creates database if he doesnt exist."""
        self.conn = sqlite3.connect('AMD.db')

    def create_table(self):
        """The function creates table."""
        self.conn.execute('CREATE TABLE Users(USERNAME CHAR, STATUS CHAR, SUSPICIOUS_APPS INT,'
                          ' CAMERA_ON INT, EMAIL TEXT, PASSWORD CHAR, FORGOT_PASSWORD BOOL, Check_Processes INT'
                          ' UNKNOWN_SOURCES CHAR)')
        self.conn.commit()

    def delete_table(self):
        """The function delete the table."""
        self.conn.execute('drop table if exists Users')
        self.conn.commit()

    def add_user(self, list_values):
        """The function gets user details and adds him to the table."""
        self.conn.execute("INSERT INTO USERS (USERNAME, STATUS, SUSPICIOUS_APPS, CAMERA_ON,"
                          " EMAIL, PASSWORD, FORGOT_PASSWORD, Check_Processes, UNKNOWN_SOURCES)"
                          " VALUES(?,?,?,?,?,?,?,?,?)", list_values)
        self.conn.commit()

    def get_user(self, username):
        """The function return user details."""
        cursor = self.conn.execute("SELECT * FROM USERS WHERE USERNAME = ?", (username,))
        for row in cursor:
            if row is None:
                break
            return row
        cursor = self.conn.execute("SELECT * FROM USERS WHERE EMAIL = ?", (username,))
        for row in cursor:
            return row

    def delete_user(self, username):
        """The function delete the user from the table."""
        self.conn.execute("DELETE FROM USERS WHERE USERNAME = ?", (username,))
        self.conn.commit()

    def add_column(self, column, column_type):
        """The function add column to the table."""
        self.conn.execute("ALTER TABLE USERS ADD COLUMN {cn} {ct}".format(cn=column, ct=column_type))
        self.conn.commit()

    def update_user(self, username, column, value):
        """The function gets username, column to change and value, abd update the table."""
        self.conn.execute("UPDATE USERS set " + column + " = ? " + " WHERE USERNAME = ?", (value, username))
        self.conn.commit()

    def get_all_users(self):
        """The function return all the details of the users from the table."""
        cursor = self.conn.execute("SELECT * FROM USERS")
        self.conn.commit()
        return cursor

    def execute(self, sql):
        """The function gets sql command and execute it."""
        cursor = self.conn.execute(sql)
        self.conn.commit()
        return cursor

    def num_rows(self):
        """The function return the number of the rows in the table."""
        cursor = self.conn.execute("SELECT COUNT(USERNAME) FROM Users")
        for row in cursor:
            return row[0]

    def close(self):
        """The function close the connection with the databse."""
        self.conn.close()
