from . import Frame
from . import FrameQueue
import cv2
from datetime import datetime, timedelta

class WebcameraSource():
    def __init__(self, url: str, N_FRAME_BEFORE_DETECTED = 500, WEBCAMERA_FPS = 24) -> None:
        self.url = url
        self.source = cv2.VideoCapture(url)

        self.fps = WEBCAMERA_FPS
        w = int(self.source.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(self.source.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.size = (w, h)
        self.fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        self.queue = FrameQueue.FrameQueue(maxlen = N_FRAME_BEFORE_DETECTED)

    def createFrame(self) -> Frame.Frame | None:
        ret, frame = self.source.read()
        if ret == False:
            return None

        x = Frame.Frame(frame, int(self.source.get(cv2.CAP_PROP_POS_FRAMES)))

        self.queue.enqueue(x)

        return x

    def flash(self, path: str, count: int, detectmotion):
        video = cv2.VideoWriter(path, self.fourcc, self.fps, self.size, True)

        while frame := self.queue.dequeue():
            video.write(frame.frame)

        current = 0
        while frame := self.createFrame():

            frame = self.queue.dequeue()
            ret, frame = detectmotion.detect(frame)
            if ret:
                current = 0

            if current >= count:
                break

            video.write(frame.frame)
            current += 1

        video.release()

    def record(self, path: str, record_minutes: int = 10) -> bool:
        start = datetime.now()
        stop = start + timedelta(minutes=record_minutes)

        video = cv2.VideoWriter(path, self.fourcc, self.fps, self.size, True)

        while frame := self.createFrame():
            video.write(frame.frame)
            if datetime.now() >= stop:
                break

        video.release()

        return True if frame != None else False