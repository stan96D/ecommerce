from abc import ABC, abstractmethod


class BaseAddressFormatter(ABC):

    @abstractmethod
    def format(address):
        pass


class NewLineAddressFormatter(BaseAddressFormatter):

    def format(self, address):
        # Split address into lines
        lines = address.split('\n')
        # Join lines with HTML line breaks
        formatted_address = '<br>'.join(lines)
        return formatted_address
