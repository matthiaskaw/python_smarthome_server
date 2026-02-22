import sqlite3
import logging
import csv
import io


from typing import List, Dict, Any
from interfaces.IDataManager import IDataManager
from interfaces.IDataService import IDataService
from datetime import datetime

#database_columns = ["IP_DateTime", "IPAddress", "DateTime", "ClientName","Temperature", "Humidity", "ModuleVoltage"]

class DatabaseManager(IDataManager, IDataService):
    
    def __init__(self, connection_string : str, database_columns : list):
        
        self._connection_string = connection_string
        #self._connection = sqlite3.connect(connection_string)
        #self._cursor = self._connection.cursor()
        self._logger = logging.getLogger(__name__)
        self._database_columns = database_columns    
        self._table_name = "sensor_data"
        self._datetime_columnname = self._database_columns[2]
        self._create_table_if_not_existing()


    async def Get_CSV_By_Date(self, start_date, end_date):



        connection = sqlite3.connect(self._connection_string)
        cursor = connection.cursor()
        start = datetime.strptime(start_date + "-01", "%Y-%m-%d")
        end   = datetime.strptime(end_date + "-01", "%Y-%m-%d")

        # nächster Monatsanfang
        if end.month == 12:
            end = end.replace(year=end.year + 1, month=1)
        else:
            end = end.replace(month=end.month + 1)

        try:
            cursor.execute(f"SELECT * FROM {self._table_name} WHERE DateTime >= ? AND DateTime < ?", (start, end))
        
            data_rows = cursor.fetchall()
            columns = [ description[0] for description in cursor.description ]
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            writer.writerow(columns)
            writer.writerows(data_rows)
            output.seek(0)
            return output
        
        except Exception as e:
            self._logger.error(f"Failed to Get CSV by date: {e}")
            
        
        finally:
            connection.close()
    
        

    



    async def Get_Data_Group_Data_By(self, field) -> List[Dict[str, Any]]:
        
        connection = sqlite3.connect(self._connection_string)
        cursor = connection.cursor()

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
        

        try:
            unique_groups = cursor.execute(unique_query_string).fetchall()
            self._logger.info(f"unique_query_string: {unique_groups}")
        


            #get the data from the last 24 hours from database
            data_query_string = f"{data_query_string} ORDER BY {self._datetime_columnname} ASC"
            self._logger.info(data_query_string)
            queried_data = cursor.execute(data_query_string).fetchall()


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
        except sqlite3.Error as e:
            self._logger.error(f"Error creating table {self._table_name}: {e}")
            
        finally:
            connection.close()  

    async def Save_Data(self, data):
        

        connection = sqlite3.connect(self._connection_string)
        cursor = connection.cursor()
        
     
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
        try:
            cursor.execute(query, values)
            connection.commit()
            
        except sqlite3.Error as e:
            self._logger.error(f"Error creating table {self._table_name}: {e}")
            raise

        finally:
            connection.close()   

    def Query_Latest_Data(self, num_rows) -> list:
        #Change function to be more generic / just for querying which can be used for downloading data
        
        #SQL Query strings limits the amount of data
        connection = sqlite3.connect(self._connection_string)
        cursor = connection.cursor()
        
        query_string = f"SELECT * FROM {self._table_name} WHERE {self._datetime_columnname} >= datetime('now', '-24 hours') ORDER BY {self._datetime_columnname} ASC"
        self._logger.info(query_string)
        
        try:
            cursor.execute(query_string)
            queried_data = cursor.fetchall()

            json_data = []    

            for row in queried_data:
                row_dict = {}
                for i, columname in enumerate(self._database_columns):
                    row_dict[columname] = row[i]
                json_data.append(row_dict)
                
        except sqlite3.Error as e:
            self._logger.error(f"Error creating table {self._table_name}: {e}")
            

        finally:
            connection.close()    

    # private methods
    
    def _create_table_if_not_existing(self):
            """Create table with dynamically selected columns"""
            # Build column definitions from selected names
            

            connection = sqlite3.connect(self._connection_string)
            cursor = connection.cursor()
            

            column_definitions = []
            for name in self._database_columns:
                column_definitions.append(f"{name}")

            columns_sql = ", ".join(column_definitions)

            try:
                create_table_sql = f"CREATE TABLE IF NOT EXISTS {self._table_name} ({columns_sql})"
                cursor.execute(create_table_sql)
                connection.commit()
                self._logger.info(f"Table {self._table_name} created with columns: {self._database_columns}")
                
            except sqlite3.Error as e:
                self._logger.error(f"Error creating table {self._table_name}: {e}")
                raise
            
            finally:
                connection.close()
            

    