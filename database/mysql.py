import pymysql
import pymysql.cursors
from util import Singleton

from environments.variables import MYSQL_HOST, MYSQL_ID, MYSQL_PASSWORD, MYSQL_DATABASE

class MySQLClient(metaclass=Singleton):
    def __init__(self, mysql_host=MYSQL_HOST, mysql_user=MYSQL_ID, mysql_password=MYSQL_PASSWORD, mysql_database=MYSQL_DATABASE):
        #host = "127.0.0.1"
        print(f"Client : host-[{mysql_host}] id-[{mysql_user}] database-[{mysql_database}]")
        self.connection = pymysql.connect(host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database=mysql_database,
            cursorclass=pymysql.cursors.DictCursor)

    def get_cursor(self):
        return self.connection.cursor()
    
    def commit(self):
        return self.connection.commit()
    
    def close(self):
        self.connection.close()