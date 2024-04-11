from abc import ABC, abstractmethod


class DatabaseImportServiceInterface(ABC):
    @abstractmethod
    def import_product_data(self, json):
        pass
