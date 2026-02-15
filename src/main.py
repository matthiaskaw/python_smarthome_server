import logging
import asyncio

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
    
    dataVisualizer = DataVisualizer()
        
    logger.info("Instantiated DataVisualizer!")
    


    logger.info("Instantiating DataHandler...")
    
    dataHandler = DataHandler(databaseManager, dataVisualizer)
    await dataHandler.run("localhost", 8080)

if __name__ == "__main__":
    asyncio.run(main())



