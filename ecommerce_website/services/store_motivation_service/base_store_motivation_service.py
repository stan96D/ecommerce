from abc import ABC, abstractmethod


class StoreMotivationInterface(ABC):

    @abstractmethod
    def get_all_motivations(self):
        pass
