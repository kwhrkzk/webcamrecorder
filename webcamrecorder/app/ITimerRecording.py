from abc import ABCMeta, abstractmethod

class ITimerRecording(metaclass=ABCMeta):
    @abstractmethod
    def record(self):
        pass