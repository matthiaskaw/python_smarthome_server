import sqlite3
import logging

from interfaces.IDataManager import IDataManager


class DatabaseManager(IDataManager):
    
    def __init__(self, connection_string : str, database_columns : list):
        
        self._connection = sqlite3.connect(connection_string)
        self._cursor = self._connection.cursor()
        self._logger = logging.getLogger(__name__)
        self._database_columns = database_columns    
        self._table_name = "sensor_data"
        self._create_table_if_not_existing()

    
    async def Save_Data(self, data):
        
     
        values = [ data[column] for column in self._database_columns]
        placeholders = ", ".join("?" for _ in self._database_columns)
        column_string = ", ".join(self._database_columns)

        query = ("INSERT INTO " 
                + self._table_name
                + " ("
                + column_string
                + ") VALUES ("
                + placeholders
                +")"
                )
        

        self._logger.info(f"Inserting {values} into {self._table_name}")

        self._cursor.execute(query, values)
        self._connection.commit()
        

    def Query_Data(query_string):
        pass

    # private methods
    
    def _create_table_if_not_existing(self):
            """Create table with dynamically selected columns"""
            # Build column definitions from selected names
            column_definitions = []
            for name in self._database_columns:
                column_definitions.append(f"{name}")

            columns_sql = ", ".join(column_definitions)

            try:
                create_table_sql = f"CREATE TABLE IF NOT EXISTS {self._table_name} ({columns_sql})"
                self._cursor.execute(create_table_sql)
                self._connection.commit()
                self._logger.info(f"Table {self._table_name} created with columns: {self._database_columns}")
            except sqlite3.Error as e:
                self._logger.error(f"Error creating table {self._table_name}: {e}")
                raise