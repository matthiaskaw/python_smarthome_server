import logging
from pathlib import Path

from interfaces.ILiveData import ILiveData
from fastapi import FastAPI, APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse




class DataVisualizer(ILiveData):
    
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.info("DataVisualizer constructor called...")
        self.router = APIRouter() 
        
        # Set up templates directory
        templates_dir = Path(__file__).parent.parent / "templates"
        self.templates = Jinja2Templates(directory=str(templates_dir))
        
        self._set_endpoints()
        
    

    async def New_Data(self,data):
        self._logger.info(f"Got new data = {data}")
        

    # private methods

    def _set_endpoints(self):
        
        self._logger.info("Setting API endpoints")
        self.router.add_api_route("/", self._root, methods=["GET"])
        self.router.add_api_route("/data", self._data_page, methods=["GET"])
        self.router.add_api_route("/visualization", self._visualization_page, methods=["GET"])
        self.router.add_api_route("/settings", self._settings_page, methods=["GET"])
        
    async def _root(self, request: Request):
        
        self._logger.info("_root called")
        return self.templates.TemplateResponse("index.html", {"request": request})
    
    async def _data_page(self, request: Request):
        self._logger.info("_data_page called")
        return self.templates.TemplateResponse("data.html", {"request": request, "page_title": "Data Monitoring"})
    
    async def _visualization_page(self, request: Request):
        self._logger.info("_visualization_page called")
        return self.templates.TemplateResponse("visualization.html", {"request": request, "page_title": "Data Visualization"})
    
    async def _settings_page(self, request: Request):
        self._logger.info("_settings_page called")
        return self.templates.TemplateResponse("settings.html", {"request": request, "page_title": "Settings"})