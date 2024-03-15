from abc import ABC, abstractmethod


class ViewServiceInterface(ABC):
    @abstractmethod
    def generate(self, items):
        pass

