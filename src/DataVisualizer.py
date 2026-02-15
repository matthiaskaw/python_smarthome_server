import logging

from interfaces.ILiveData import ILiveData




class DataVisualizer(ILiveData):
    
    def __init__(self):
        self._logger = logging.getLogger(__name__)
    

    async def New_Data(self,data):
        self._logger.info(f"Got new data = {data}")