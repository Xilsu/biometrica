import sqlite3

class Service():
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
    
    def select(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        
        info = cursor.fetchall()
        
        self.connection.commit()
        
        return cursor, info
    
    def insert(self, query, data):
        cursor = self.connection.cursor()
        cursor.execute(query, data)
        
        self.connection.commit()
    
    def close(self):
        self.connection.close()