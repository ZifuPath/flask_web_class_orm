from abc import ABC,abstractmethod

class UserService(ABC):

    @abstractmethod
    def add_user(self):
        pass

    @abstractmethod
    def update_user(self):
        pass

    @abstractmethod
    def get_user(self):
        pass

    @abstractmethod
    def get_all_user(self):
        pass

    @abstractmethod
    def delete_user(self):
        pass
