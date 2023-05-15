import cv2


class Frame:
    def __init__(self, frame, frame_position) -> None:
        self.frame = frame
        self.frame_position = frame_position

    def write(self, path: str) -> bool:
        return cv2.imwrite(path, self.frame)

    def encode(self) -> bytes:
        ret, num_bytes = cv2.imencode(".jpg", self.frame)
        return num_bytes.tobytes()
