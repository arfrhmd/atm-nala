from config.colors import colors
import mysql.connector

class Database:
    def __init__(self, host='localhost', user='root', passwd='', db='atm'):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = db
        self.conn = None
        
        
    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.passwd,
                database=self.database
            )
            self.cur = self.conn.cursor(dictionary=True)
        except Exception as err:
            print(f"{colors.FAIL}DB ERROR: {err}{colors.ENDC}")
    
    
    def insert(self, sql, val):
        try:
            self.cur.execute(sql, val)
            self.conn.commit()
        except Exception as err:
            print(f"{colors.FAIL}DB ERROR: {err}{colors.ENDC}")
            
    
    def read(self, mode, sql, val=None):
        try:
            if mode == 'one':
                try:
                    if val:
                        self.cur.execute(sql, val)
                    else:
                        self.cur.execute(sql)
                        
                    return self.cur.fetchone()
                except Exception as err:
                    print(f"{colors.FAIL}DB ERROR: {err}{colors.ENDC}")
            elif mode == 'all':
                try:
                    if val:
                        self.cur.execute(sql, val)
                    else:
                        self.cur.execute(sql)
                        
                    return self.cur.fetchall()
                except Exception as err:
                    print(f"{colors.FAIL}DB ERROR: {err}{colors.ENDC}")
            else:
                raise ValueError("value of argument 'mode' in Database.read() is not found")
        except ValueError as err:
            print(f"{colors.FAIL}APP ERROR: {err}{colors.ENDC}")
            
            
    def update(self, sql, val):
        try:
            self.cur.execute(sql, val)
            self.conn.commit()
        except Exception as err:
            print(f"{colors.FAIL}DB ERROR: {err}{colors.ENDC}")
                      
            
    def close(self):
        self.conn.close()
        