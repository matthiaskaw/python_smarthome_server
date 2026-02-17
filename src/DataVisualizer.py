import logging
from pathlib import Path
from interfaces.IDataService import IDataService
from interfaces.ILiveData import ILiveData
from fastapi import FastAPI, APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse




class DataVisualizer():
    
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
        
    async def _root(self, request: Request):
        
        return self.templates.TemplateResponse("index.html", {
            "request": request
        })
    

    async def _get_data(self):
        #Replace hardcoded grouping field with dynamic group field
        
        latest_data = self._dataManager.Get_Data_Group_Data_By("ClientName")
        self._logger.info(latest_data)
        return latest_data
        