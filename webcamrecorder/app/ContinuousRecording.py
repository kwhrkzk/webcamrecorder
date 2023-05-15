from . import IContinuousRecording
from ..domain.WebcameraSource import WebcameraSource
import os
from dotenv import load_dotenv
import datetime


class ContinuousRecording(IContinuousRecording.IContinuousRecording):
    def __init__(self) -> None:
        load_dotenv()

        self.WEBCAMERA_RECORD_MINUTES = int(
            os.getenv("WEBCAMERA_RECORD_MINUTES") or 10000
        )
        self.WEBCAMERA_OUTPUTFILENAME = os.getenv("WEBCAMERA_OUTPUTFILENAME")
        self.source = WebcameraSource(
            os.getenv("WEBCAMERA_URL"),
            int(os.getenv("N_FRAME_BEFORE_DETECTED") or "0"),
            int(os.getenv("WEBCAMERA_FPS") or "24"),
        )

    def record(self):
        while True:
            now = format(datetime.datetime.now(), "%Y%m%d%H%M%S")
            filepath = os.path.join(
                "store", self.WEBCAMERA_OUTPUTFILENAME + "_" + now + ".mp4"
            )
            ret = self.source.record(filepath, self.WEBCAMERA_RECORD_MINUTES)
            if not ret:
                break
