from abc import ABC, abstractmethod


class PixelsDiceMachineInterface(ABC):

    @property
    @abstractmethod
    def isConnected(self) -> bool:
        pass

    @abstractmethod
    def start(self):
        pass
