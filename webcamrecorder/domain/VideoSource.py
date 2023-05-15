from . import Frame
from . import FrameQueue
import cv2


class VideoSource():
    def __init__(self, path: str, N_FRAME_BEFORE_DETECTED=500):
        self.path = path
        self.source = cv2.VideoCapture(path)

        self.frame_count = int(self.source.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(self.source.get(cv2.CAP_PROP_FPS))
        w = int(self.source.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(self.source.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.size = (w, h)
        self.fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        self.queue = FrameQueue.FrameQueue(maxlen=N_FRAME_BEFORE_DETECTED)

    def createFrame(self, frame_count=-1) -> Frame.Frame | None:
        if frame_count != -1:
            self.source.set(cv2.CAP_PROP_POS_FRAMES, frame_count)

        ret, frame = self.source.read()
        if not ret:
            return None

        x = Frame.Frame(frame, int(self.source.get(cv2.CAP_PROP_POS_FRAMES)))

        self.queue.enqueue(x)

        return x

    def flash(self, path: str, count: int, detectmotion):
        video = cv2.VideoWriter(path, self.fourcc, self.fps, self.size, True)

        while frame := self.queue.dequeue():
            video.write(frame.frame)

        current_frame_pos = int(self.source.get(cv2.CAP_PROP_POS_FRAMES))

        max = self.frame_count if current_frame_pos + count >= self.frame_count else current_frame_pos + count

        while frame := self.createFrame():

            frame = self.queue.dequeue()
            ret, frame = detectmotion.detect(frame)
            if ret:
                max = self.frame_count if frame.frame_position + count >= self.frame_count else frame.frame_position + count

            if frame.frame_position >= max:
                break

            video.write(frame.frame)

        video.release()
