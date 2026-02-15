from abc import ABC, abstractmethod


class ILiveData(ABC):
    
    @abstractmethod
    async def New_Data(data : dict):
        pass