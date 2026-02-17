import logging
import asyncio
import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles

from src.DatabaseManager import DatabaseManager
from src.DataHandler import DataHandler
from src.DataVisualizer import DataVisualizer


async def main():
    

    host_name = "0.0.0.0"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)

    logger.info("Starting Application...")


    logger.info("Instantiating DatabaseManager...")
    
    database_columns = ["IP_DateTime", "IPAddress", "DateTime", "ClientName","Temperature", "Humidity", "ModuleVoltage"]
    databaseManager = DatabaseManager("sensor_database.db", database_columns)
    logger.info("Instantiated DatabaseManager!")
    


    logger.info("Instantiating DataVisualizer...")
    
    app = FastAPI()
    conf = uvicorn.Config(app, host=host_name, port=8000)
    server = uvicorn.Server(conf)

    dataVisualizer = DataVisualizer(databaseManager, database_columns)
    app.include_router(dataVisualizer.router)
    app.mount("/static/javascripts",StaticFiles(directory="wwwroot/static/javascripts"), name="javascripts")
    app.mount("/static/css", StaticFiles(directory="wwwroot/static/css"), name="css")
    logger.info("Instantiated DataVisualizer!")
    

    


    logger.info("Instantiating DataHandler...")
    
    dataHandler = DataHandler(databaseManager)
    await asyncio.gather(
        dataHandler.run(host_name, 8080),
        server.serve()
    )
    
if __name__ == "__main__":
    asyncio.run(main())



