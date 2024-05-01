from abc import ABC, abstractmethod


class ViewServiceInterface(ABC):
    @abstractmethod
    def generate(self, items):
        pass

    @abstractmethod
    def get(self, item):
        pass


class SingleViewServiceInterface(ABC):

    @abstractmethod
    def get(self, item):
        pass


class EmptyViewServiceInterface(ABC):

    @abstractmethod
    def get_single(self, item):
        pass
