import asyncio
import logging
import json
from websockets.asyncio.server import serve
from interfaces.IDataManager import IDataManager
from interfaces.ILiveData import ILiveData
from datetime import datetime



class DataHandler:

    # public methods
    
    def __init__(self, dataManager : IDataManager):
        
        self._logger = logging.getLogger(__name__)
        self._logger.info("Constructing dataHandler")
        self._dataManager = dataManager
        
        

    async def run(self, host_ip : str, port : int):
        
        async with serve(self._receiveDataHandler, host_ip, port) as server:
            await server.serve_forever()
            
        self._logger("End of run in DataHandler")

    # private methods
    
    async def _receiveDataHandler(self, websocket):
        
        async for message in websocket:
            self._logger.info("Getting data from websocket client...")
            data = json.loads(message)
            self._logger.info(f"client ip = {websocket.remote_address[0]}")
            data["IP_DateTime"] = f"{websocket.remote_address[0]}_{datetime.now()}"
            data["IPAddress"] = f"{websocket.remote_address[0]}"
            data["DateTime"] = f"{datetime.now()}"
            
            await asyncio.gather(
                self._dataManager.Save_Data(data),
            )       


if __name__ == "__main__":
    
    print("Testing DataHandler class...")
    
    