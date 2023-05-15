from abc import ABCMeta, abstractmethod
from ..domain.Frame import Frame


class ISendMail(metaclass=ABCMeta):
    @abstractmethod
    def send(self, frame: Frame, subect: str = "subject", body: str = "body"):
        pass
