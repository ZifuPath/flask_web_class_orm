from abc import ABC,abstractmethod

class BatchService(ABC):

    @abstractmethod
    def add_batch(self):
        pass

    @abstractmethod
    def update_batch(self):
        pass

    @abstractmethod
    def get_batch(self):
        pass

    @abstractmethod
    def get_all_batch(self):
        pass

    @abstractmethod
    def delete_batch(self):
        pass
    #
    @abstractmethod
    def assign_student(self):
        pass