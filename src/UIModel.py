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



class UIModel():
    
    def __init__(self, dataManager : IDataService, database_columns : list):
        
        self._logger = logging.getLogger(__name__)
        self._logger.info("DataVisualizer constructor called...")
        
        self._dataManager = dataManager
        self._database_columns = database_columns
        
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
        self.router.add_api_route("/download", self._download_data, methods=["GET"])
        self.router.add_api_route("/api/timeframe", self._get_timeframed_data, methods=["GET"])
        



    async def _root(self, request: Request):
        latest_data = await self._dataManager.Get_Data_Group_Data_By("ClientName")
        keys = list(latest_data.keys())
        return self.templates.TemplateResponse("index.html", {
            "request": request, "groups" : keys
        })
    

    async def _download_data(self, request : Request):
        

        return self.templates.TemplateResponse("download.html", {"request":request})
    

    async def _get_data(self):
        #Replace hardcoded grouping field with dynamic group field
        
        latest_data = await self._dataManager.Get_Data_Group_Data_By("ClientName")
        #self._logger.info(latest_data)
        return latest_data
    
    async def _get_timeframed_data(self, start_month : str = Query(...), end_month : str = Query(...)):
        
            
        try:

           csv_output = await self._dataManager.Get_CSV_By_Date(start_month, end_month)
           self._logger.info(f"Type of csv: {type(csv_output)}")
           return StreamingResponse(
            
            csv_output,
            media_type="text/csv",
            headers={"Content-Disposition" : "attachment; filename=sensordata.csv"}
            
        )
        except Exception as e:
                self._logger.error(f"Error: {e}")
                raise
      