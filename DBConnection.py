import mysql.connector


class Db:
    def __init__(self,user,database):
        self.cnx = mysql.connector.connect(host="localhost", user=user, password="", database=database)
        self.cur = self.cnx.cursor(dictionary=True)

    def select(self, q):
        self.cur.execute(q)
        return self.cur.fetchall()

    def selectOne(self, q):
        self.cur.execute(q)
        return self.cur.fetchone()

    def insert(self, q):
        self.cur.execute(q)
        self.cnx.commit()
        return self.cur.lastrowid

    def update(self, q):
        self.cur.execute(q)
        self.cnx.commit()
        return self.cur.rowcount

    def delete(self, q):
        self.cur.execute(q)
        self.cnx.commit()
        return self.cur.rowcount
