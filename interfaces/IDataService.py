from abc import ABC, abstractmethod
import io

from typing import List, Dict, Any


class IDataService(ABC):
    
    @abstractmethod
    async def Get_Data_Group_Data_By(field : str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def Get_CSV_By_Date(start_date : str, end_date : str) -> io.StringIO:
        pass
    
    
    


