import pyodbc
from typing import Optional

server = 'IN-BWF3NX3'
database = 'EmployeeDatabase'
username = 'sa'
password = 'sa'
driver = '{ODBC Driver 17 for SQL Server}'

class DatabaseManager:
    def __init__(self, server: str, database: str, username: str, password: str, driver: str):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.driver = driver

    def create_connection(self) -> pyodbc.Connection:
        return pyodbc.connect(
            f'DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}'
        )

    def fetch_all(self, query: str, params: Optional[tuple] = None) -> list:
        connection = self.create_connection()
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        rows = cursor.fetchall()
        connection.close()
        return rows

    def execute_query(self, query: str, params: Optional[tuple] = None):
        connection = self.create_connection()
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        connection.commit()
        connection.close()
