import mysql.connector as mariadb

class Score:

    def __init__(self, cursor, ark = ''):
        self.ark = ark;
        self.cursor = cursor

    def get_all(self, limit = 50):
        self.cursor.execute("SELECT * from glc_partition",(limit))
        return self.cursor.fetchall()

    def get_byid(self, id):
        self.cursor.execute('SELECT * FROM glc_partition where ark = "%s"',(id))
        return self.cursor.fetchall()

    def search(self, query):
        sql = "SELECT * FROM glc_metadata WHERE LOWER(value) like %s"
        self.cursor.execute(sql, ("%" + query + "%",))
        return self.cursor.fetchall()
