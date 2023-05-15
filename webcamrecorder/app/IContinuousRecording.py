from abc import ABCMeta, abstractmethod

class IContinuousRecording(metaclass=ABCMeta):
    @abstractmethod
    def record(self):
        pass