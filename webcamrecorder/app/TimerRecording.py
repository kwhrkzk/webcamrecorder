from . import ITimerRecording
from ..domain.WebcameraSource import WebcameraSource
import os
from dotenv import load_dotenv
import datetime


class TimerRecording(ITimerRecording.ITimerRecording):
    def __init__(self) -> None:
        load_dotenv()

        self.record_minutes = int(os.getenv("WEBCAMERA_RECORD_MINUTES") or 10)
        self.output_file_name = os.getenv("WEBCAMERA_OUTPUTFILENAME")
        self.source = WebcameraSource(
            os.getenv("WEBCAMERA_URL"),
            int(os.getenv("N_FRAME_BEFORE_DETECTED") or 0),
            int(os.getenv("WEBCAMERA_FPS") or 24))

    def record(self):
        now = format(datetime.datetime.now(), "%Y%m%d%H%M%S")
        filepath = os.path.join(
            "store",
            self.output_file_name + "_" + now + ".mp4")
        self.source.record(filepath, self.record_minutes)
