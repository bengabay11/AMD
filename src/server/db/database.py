import sqlite3
from src.server import config


class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect(config.DB_FILE_PATH)

    def create_table(self):
        self.conn.execute('CREATE TABLE Users(USERNAME CHAR, STATUS CHAR, SUSPICIOUS_APPS INT,'
                          ' CAMERA_ON INT, EMAIL TEXT, PASSWORD CHAR, FORGOT_PASSWORD BOOL, Check_Processes INT'
                          ' UNKNOWN_SOURCES CHAR)')
        self.conn.commit()

    def delete_table(self):
        self.conn.execute('drop table if exists Users')
        self.conn.commit()

    def add_user(self, list_values):
        self.conn.execute("INSERT INTO USERS (USERNAME, STATUS, SUSPICIOUS_APPS, CAMERA_ON,"
                          " EMAIL, PASSWORD, FORGOT_PASSWORD, Check_Processes, UNKNOWN_SOURCES)"
                          " VALUES(?,?,?,?,?,?,?,?,?)", list_values)
        self.conn.commit()

    def get_user(self, username):
        cursor = self.conn.execute("SELECT * FROM USERS WHERE USERNAME = ?", (username,))
        for row in cursor:
            if row is None:
                break
            return row
        cursor = self.conn.execute("SELECT * FROM USERS WHERE EMAIL = ?", (username,))
        for row in cursor:
            return row

    def delete_user(self, username):
        self.conn.execute("DELETE FROM USERS WHERE USERNAME = ?", (username,))
        self.conn.commit()

    def add_column(self, column, column_type):
        self.conn.execute("ALTER TABLE USERS ADD COLUMN {cn} {ct}".format(cn=column, ct=column_type))
        self.conn.commit()

    def update_user(self, username, column, value):
        self.conn.execute("UPDATE USERS set " + column + " = ? " + " WHERE USERNAME = ?", (value, username))
        self.conn.commit()

    def get_all_users(self):
        cursor = self.conn.execute("SELECT * FROM USERS")
        self.conn.commit()
        return cursor

    def execute(self, sql):
        cursor = self.conn.execute(sql)
        self.conn.commit()
        return cursor

    def num_rows(self):
        cursor = self.conn.execute("SELECT COUNT(USERNAME) FROM Users")
        for row in cursor:
            return row[0]

    def close(self):
        self.conn.close()
