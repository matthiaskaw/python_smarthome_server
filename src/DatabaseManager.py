import sqlite3
import logging
from typing import List, Dict, Any
from interfaces.IDataManager import IDataManager
from interfaces.IDataService import IDataService
#database_columns = ["IP_DateTime", "IPAddress", "DateTime", "ClientName","Temperature", "Humidity", "ModuleVoltage"]

class DatabaseManager(IDataManager, IDataService):
    
    def __init__(self, connection_string : str, database_columns : list):
        
        self._connection = sqlite3.connect(connection_string)
        self._cursor = self._connection.cursor()
        self._logger = logging.getLogger(__name__)
        self._database_columns = database_columns    
        self._table_name = "sensor_data"
        self._datetime_columnname = self._database_columns[2]
        self._create_table_if_not_existing()

    async def Get_Data_Group_Data_By(self, field) -> List[Dict[str, Any]]:
        

        #Check if 'field' exists
        grouping_field = "None"
        
        for columnname in self._database_columns:
            if(columnname == field):
                grouping_field = field
                
        if(grouping_field == "None"):
            self._logger.error(f"Field not in table. Cannot provide grouped data. Passes field is {field}")
            return List[Dict[str, Any]]()
        
        #atomic approach for data querying: split unique (-> get unique groups) and data query
        
        #get unique groups
        data_query_string = f"SELECT * FROM {self._table_name} WHERE {self._datetime_columnname} >= datetime('now', '-24 hours')"

        unique_query_string = f"SELECT DISTINCT {grouping_field} FROM ({data_query_string})"
        unique_groups = self._cursor.execute(unique_query_string).fetchall()
        self._logger.info(f"unique_query_string: {unique_groups}")
        


        #get the data from the last 24 hours from database
        data_query_string = f"{data_query_string} ORDER BY {self._datetime_columnname} ASC"
        self._logger.info(data_query_string)
        queried_data = self._cursor.execute(data_query_string).fetchall()


        #group data by client name field
  
        grouped_data = {}
        for group in unique_groups:
            group = group[0]
            self._logger.info(group)
            single_data_in_group = []
            
            json_data = []    

            for row in queried_data:
                if(row[3] == group):
 
                    row_dict = {}
                    for i, columname in enumerate(self._database_columns):
                        row_dict[columname] = row[i]
                    json_data.append(row_dict)
                    
                grouped_data[group] = json_data
        return grouped_data    

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
        

    def Query_Latest_Data(self, num_rows) -> list:
        #Change function to be more generic / just for querying which can be used for downloading data
        
        #SQL Query strings limits the amount of data
        query_string = f"SELECT * FROM {self._table_name} WHERE {self._datetime_columnname} >= datetime('now', '-24 hours') ORDER BY {self._datetime_columnname} ASC"
        self._logger.info(query_string)
        self._cursor.execute(query_string)
        queried_data = self._cursor.fetchall()

        json_data = []    

        for row in queried_data:
            row_dict = {}
            for i, columname in enumerate(self._database_columns):
                row_dict[columname] = row[i]
            json_data.append(row_dict)
             
        return json_data
        

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