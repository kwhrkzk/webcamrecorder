from . import IDetectMotion
from ..domain.Frame import Frame
import cv2


class DetectMotion(IDetectMotion.IDetectMotion):
    def __init__(self) -> None:
        self.backgroundsubtractor = cv2.bgsegm.createBackgroundSubtractorMOG()
        pass

    def detect(self, frame: Frame) -> tuple[bool, Frame]:
        clone = frame.frame.copy()
        mask = self.backgroundsubtractor.apply(clone)

        # Mask the bottom left.
        # mask = cv2.rectangle(mask, (0, 180), (300, 720), (0,0,0), -1)

        contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

        # remove small contours.
        contours = list(filter(lambda x: cv2.contourArea(x) > 500, contours))

        bboxes = list(map(lambda x: cv2.boundingRect(x), contours))

        for x, y, w, h in bboxes:
            cv2.rectangle(clone, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return (
            (False, frame)
            if len(bboxes) == 0
            else (True, Frame(clone, frame.frame_position))
        )
