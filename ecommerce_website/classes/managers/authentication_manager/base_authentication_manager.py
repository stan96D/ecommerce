from abc import ABC, abstractmethod


class AuthenticationInterface(ABC):
    @abstractmethod
    def login(self, request, email, password):
        pass

    @abstractmethod
    def logout(self, request):
        pass

