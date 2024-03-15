from abc import ABC, abstractmethod


class BaseHandlerInterface(ABC):
    @property
    @abstractmethod
    def data(self):
        pass

    @property
    @abstractmethod
    def count(self):
        pass
