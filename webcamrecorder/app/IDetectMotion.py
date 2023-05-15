from abc import ABCMeta, abstractmethod
from ..domain.Frame import Frame


class IDetectMotion(metaclass=ABCMeta):
    @abstractmethod
    def detect(self, frame: Frame) -> tuple[bool, Frame]:
        pass
