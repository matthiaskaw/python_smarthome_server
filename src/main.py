import logging
import asyncio
import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles

from src.DatabaseManager import DatabaseManager
from src.DataHandler import DataHandler
from src.UIModel import UIModel


async def main():
    


    database_name = "sensor_database.db"

    host_name = "0.0.0.0"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)

    logger.info("Starting Application...")


    logger.info("Instantiating DatabaseManager...")
    
    database_columns_room_sensors = ["IP_DateTime", "IPAddress", "DateTime", "ClientName","Temperature", "Humidity", "ModuleVoltage"]
    databaseManager_room_sensors = DatabaseManager(database_name, database_columns_room_sensors, table_name="room_sensors")
    logger.info("Instantiated DatabaseManager for Room Sensors!")
    
    database_columns_solar_sensor = ["IP_DateTime", "IPAddress", "DateTime", "ClientName", "Solar_Cell_Voltage", "Voltage_1", "Voltage_2", "Voltage_3", "Voltage_4", "Voltage_5"]
    databaseManager_solar_sensor = DatabaseManager(database_name, database_columns=database_columns_solar_sensor, table_name="solar_sensor")
    logger.info("Instantiated DatabaseManager for Solar Sensor!")


    logger.info("Instantiating DataVisualizer...")
    
    app = FastAPI()
    conf = uvicorn.Config(app, host=host_name, port=8000)
    server = uvicorn.Server(conf)

    dataVisualizer = UIModel(databaseManager_room_sensors,
                             database_columns_room_sensors,
                             dataManager_solar_charger=databaseManager_solar_sensor,
                             database_solar_charger_columns=database_columns_solar_sensor)
    
    app.include_router(dataVisualizer.router)
    app.mount("/static/javascripts",StaticFiles(directory="wwwroot/static/javascripts"), name="javascripts")
    app.mount("/static/css", StaticFiles(directory="wwwroot/static/css"), name="css")
    logger.info("Instantiated DataVisualizer!")
    

    


    logger.info("Instantiating DataHandler...")
    
    dataHandler_room_sensor = DataHandler(databaseManager_room_sensors)
    dataHandler_solar_sensor = DataHandler(databaseManager_solar_sensor)
    await asyncio.gather(
        dataHandler_room_sensor.run(host_name, 8080),
        dataHandler_solar_sensor.run(host_name, 8070),
        server.serve() 
    )
    
    
    await asyncio.gather(
               
    )
    
if __name__ == "__main__":
    asyncio.run(main())



