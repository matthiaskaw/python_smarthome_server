from abc import ABC, abstractmethod


class IDataManager(ABC):
    

    @abstractmethod
    async def Save_Data(data : dict):
        pass


    @abstractmethod
    async def Query_Latest_Data(num_rows : int):
        pass