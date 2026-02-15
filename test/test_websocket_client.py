import asyncio
from websockets.asyncio.client import connect
import logging
from datetime import datetime
import random
import json
import time
class test_client:
    
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._name = __name__

    async def run(self):
        while True:
            timestamp = datetime.now()
            
            data = {
                
                    "IP_DateTime" : f"localhost_{timestamp}",
                    "IPAddress" : "localhost",
                    "DateTime" : f"{timestamp}",
                    "Temperature" : random.uniform(18,25),
                    "Humidity" : random.uniform(40, 50),
                    "ModuleVoltage" : random.uniform(1, 5)
                }

            async with connect("ws://localhost:8080") as websocket:
                data_string = json.dumps(data)
                self._logger.info(f"test_client json dumps {data_string}")
                await websocket.send(json.dumps(data))
                await websocket.close()
            time.sleep(2)
                


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    client = test_client()
    asyncio.run(client.run())