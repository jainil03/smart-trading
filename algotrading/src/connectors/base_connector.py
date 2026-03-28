from abc import ABC, abstractmethod

class BaseConnector(ABC):
    """
    Abstract Base Class for all Exchange Data Connectors.
    Each exchange will implement its own WebSocket/Streaming logic.
    """

    @abstractmethod
    def __init__(self, symbol: str):
        self.symbol = symbol

    @abstractmethod
    async def connect(self, callback):
        """
        Connects to the exchange's websocket.
        :param callback: An async function to process incoming market data.
        """
        pass
