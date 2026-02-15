import logging
import asyncio
import uvicorn
from fastapi import FastAPI, APIRouter
from src.DatabaseManager import DatabaseManager
from src.DataHandler import DataHandler
from src.DataVisualizer import DataVisualizer


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)

    logger.info("Starting Application...")


    logger.info("Instantiating DatabaseManager...")
    
    database_columns = ["IP_DateTime", "IPAddress", "DateTime", "Temperature", "Humidity", "ModuleVoltage"]
    databaseManager = DatabaseManager("sensor_database.db", database_columns)
    
    logger.info("Instantiated DatabaseManager!")
    


    logger.info("Instantiating DataVisualizer...")
    
    app = FastAPI()
    conf = uvicorn.Config(app, host="localhost", port=8000)
    server = uvicorn.Server(conf)

    dataVisualizer = DataVisualizer()
    app.include_router(dataVisualizer.router)
        
    logger.info("Instantiated DataVisualizer!")
    

    


    logger.info("Instantiating DataHandler...")
    
    dataHandler = DataHandler(databaseManager, dataVisualizer)
    await asyncio.gather(
        dataHandler.run("localhost", 8080),
        server.serve()
    )
    
if __name__ == "__main__":
    asyncio.run(main())



