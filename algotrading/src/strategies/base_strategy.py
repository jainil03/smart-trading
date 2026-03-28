from abc import ABC, abstractmethod

class BaseStrategy(ABC):

    @abstractmethod
    def generate_signals(self, data):
        pass
