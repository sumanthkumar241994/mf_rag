from abc import abstractmethod, ABC


class StorageProvider(ABC):
    

    @abstractmethod
    def dowload(self, bucket: str, key: str) -> str:
        """
        Downloads the file and returns the local path
        """
        raise NotImplementedError