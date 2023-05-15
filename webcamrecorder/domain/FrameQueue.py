from collections import deque
from . import Frame


class FrameQueue:
    def __init__(self, maxlen=1000) -> None:
        self.queue = deque(maxlen=maxlen)

    def enqueue(self, frame: Frame.Frame) -> None:
        self.queue.append(frame)

    def dequeue(self) -> Frame.Frame | None:
        if len(self.queue) != 0:
            return self.queue.popleft()
        else:
            return None
