import logging
from pathlib import Path
import sys 
from datetime import datetime

from interfaces.IDataService import IDataService
from interfaces.ILiveData import ILiveData
from fastapi import FastAPI, APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi import Query
import json


class UIModel():
    
    def __init__(self,
                 dataManager_room_sensors : IDataService,
                 database_room_sensor_columns : list,
                 dataManager_solar_charger : IDataService,
                 database_solar_charger_columns : list):
        
        self._logger = logging.getLogger(__name__)
        self._logger.info("DataVisualizer constructor called...")
        
        self._dataManager_room_sensors = dataManager_room_sensors
        self._database_columns = database_room_sensor_columns
        
        self._dataManager_solar_charger = dataManager_solar_charger
        self._database_solar_charger_columns = database_solar_charger_columns
        
        self.router = APIRouter() 

        # Set up templates directory
        templates_dir = Path(__file__).parent.parent / "wwwroot"
        self.templates = Jinja2Templates(directory=str(templates_dir))
        
        self._set_endpoints()
         

    # private methods

    def _set_endpoints(self):
        
        self._logger.info("Setting API endpoints")
        self.router.add_api_route("/", self._root, methods=["GET"])
        self.router.add_api_route("/api/data", self._get_data, methods=["GET"])
        self.router.add_api_route("/api/solar_charger_data", self._get_solar_charger_data, methods=["GET"])
        self.router.add_api_route("/download", self._download_data, methods=["GET"])
        self.router.add_api_route("/api/timeframe", self._get_timeframed_data, methods=["GET"])
        self.router.add_api_route("/solar_charger", self._solar_charger, methods=["GET"])
        



    async def _root(self, request: Request):
        latest_data = await self._dataManager_room_sensors.Get_Data_Group_Data_By("ClientName")
        keys = list(latest_data.keys())
        return self.templates.TemplateResponse("index.html", {
            "request": request, "groups" : keys
        })
    

    async def _download_data(self, request : Request):
        

        return self.templates.TemplateResponse("download.html", {"request":request})
    

    async def _get_data(self):
        #Replace hardcoded grouping field with dynamic group field
        
        latest_data = await self._dataManager_room_sensors.Get_Data_Group_Data_By("ClientName")
        #self._logger.info(latest_data)
        return latest_data
    
    async def _get_timeframed_data(self, start_month : str = Query(...), end_month : str = Query(...)):
        
            
        try:

           csv_output = await self._dataManager_room_sensors.Get_CSV_By_Date(start_month, end_month)
           self._logger.info(f"Type of csv: {type(csv_output)}")
           return StreamingResponse(
            
            csv_output,
            media_type="text/csv",
            headers={"Content-Disposition" : "attachment; filename=sensordata.csv"}
            
        )
        except Exception as e:
                self._logger.error(f"Error: {e}")
                raise
      


    async def _solar_charger(self, request : Request):

        latest_data, columns = await self._dataManager_solar_charger.Query_Latest_Data("1")
        # print(columns)        
        voltage_columnname = [columns[-6], columns[-5], columns[-4], columns[-3], columns[-2], columns[-1]]
        print(voltage_columnname)
        return self.templates.TemplateResponse("solar_charger.html", {
            "request": request, "voltage_names" : voltage_columnname})


    async def _get_solar_charger_data(self):
        
        latest_data, columns = await self._dataManager_solar_charger.Query_Latest_Data("1")
        # print(columns)        
        voltage_columns = [columns[-6], columns[-5], columns[-4], columns[-3], columns[-2], columns[-1]]

        #self._logger.info(latest_data)
        return [latest_data, voltage_columns]