import abc

class NifiComponent:

    @abc.abstractmethod
    def create(self):
        return