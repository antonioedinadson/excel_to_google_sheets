import sqlite3
import os

class Database:
    
    def __init__(self, table_name, columns) -> None:
        self.columns = ','.join(columns)
        self.table_name = table_name

        self._db_file = "database/excel_extract.db"
        self._connection = self.connect()
        self._cursor = self._connection.cursor()            

        # CRIAR TABELA
        self.create_table()

    def connect(self) -> sqlite3.Connection:
        try:
            return sqlite3.connect(self._db_file)
        except sqlite3.Error as e:
            raise e
        
    def close_connection(self) -> None:
        if self._connection:
            self._connection.close()        

    def create_table(self) -> None:
        try:            
            create_table = f"CREATE TABLE IF NOT EXISTS {self.table_name} (ID INTEGER PRIMARY KEY, {self.columns})"
            self._cursor.execute(create_table)
            self._connection.commit()            
        except sqlite3.Error as e:            
            raise e
        
    def insert_data(self, data) -> list:
        try:
            
            for row_data  in data:
                columns_part = ', '.join(row_data.keys())
                placeholders = ','.join(['?' for _ in range(len(row_data))])
                values = list(row_data.values())   

                insert_query = f"INSERT INTO {self.table_name} ({columns_part}) VALUES ({placeholders})"  
                self._cursor.execute(insert_query, values)
                
                last_insert_id = self._cursor.lastrowid
                print(f'EXTRACT EXCEL: {last_insert_id}')

            self._connection.commit()   
                        
        except sqlite3.Error as e:
            raise e

    def all(self) -> list:
        try:
            select_query = f"SELECT * FROM {self.table_name}"
            self._cursor.execute(select_query)
            rows = self._cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            raise e

    def _table_destroy(self, table_name):
        try:
            sql_query = f"DROP TABLE IF EXISTS {table_name};"
            self.cursor.execute(sql_query)
            self.connection.commit()
        except sqlite3.Error as e:
            raise e
