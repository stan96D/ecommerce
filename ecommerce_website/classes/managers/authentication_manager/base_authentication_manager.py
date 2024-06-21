from abc import ABC, abstractmethod


class AuthenticationInterface(ABC):
    @abstractmethod
    def login(self, request, email, password):
        pass

    @abstractmethod
    def logout(self, request):
        pass


    @abstractmethod
    def sign_up(self, request, form):
        pass

