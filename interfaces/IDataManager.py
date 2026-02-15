from abc import ABC, abstractmethod


class IDataManager(ABC):
    

    @abstractmethod
    async def Save_Data(data : dict):
        pass


    @abstractmethod
    async def Query_Data(query_string : str):
        pass