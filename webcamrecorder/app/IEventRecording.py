from abc import ABCMeta, abstractmethod


class IEventRecording(metaclass=ABCMeta):
    @abstractmethod
    def record(self):
        pass
