from abc import ABCMeta, abstractmethod


class ITimerEventRecording(metaclass=ABCMeta):
    @abstractmethod
    def record(self):
        pass
