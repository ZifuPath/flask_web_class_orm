from abc import ABC,abstractmethod

class StaffService(ABC):

    @abstractmethod
    def add_staff(self):
        pass

    @abstractmethod
    def update_staff(self):
        pass

    @abstractmethod
    def get_staff(self):
        pass

    @abstractmethod
    def get_all_staff(self):
        pass

    @abstractmethod
    def delete_staff(self):
        pass
    #
    @abstractmethod
    def assign_batch(self):
        pass
