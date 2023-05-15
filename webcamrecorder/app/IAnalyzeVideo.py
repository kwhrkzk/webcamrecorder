from abc import ABCMeta, abstractmethod

class IAnalyzeVideo(metaclass=ABCMeta):
    @abstractmethod
    def analyze(self):
        pass