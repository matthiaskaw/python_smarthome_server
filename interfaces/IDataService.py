from abc import ABC, abstractmethod

from typing import List, Dict, Any


class IDataService(ABC):
    
    @abstractmethod
    async def Get_Data_Group_Data_By(field : str) -> List[Dict[str, Any]]:
        pass



