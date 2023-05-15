from . import IAnalyzeVideo
from . import IDetectMotion
from ..domain import VideoSource
import os
from dotenv import load_dotenv
from injector import inject, noninjectable


class AnalyzeVideo(IAnalyzeVideo.IAnalyzeVideo):
    @inject
    @noninjectable("path")
    def __init__(self, detectmotion: IDetectMotion.IDetectMotion, path: str) -> None:
        load_dotenv()

        self.detectmotion = detectmotion
        self.N_FRAME_AFTER_DETECTED = int(os.getenv("N_FRAME_AFTER_DETECTED") or 500)
        self.output_file_name, _ = os.path.splitext(path)
        self.source = VideoSource.VideoSource(
            path, int(os.getenv("N_FRAME_BEFORE_DETECTED") or 0)
        )

    def analyze(self):
        while frame := self.source.createFrame():
            ret, frame = self.detectmotion.detect(frame)
            if ret:
                filepath = os.path.join(
                    "store",
                    self.output_file_name + "_" + str(frame.frame_position) + ".mp4",
                )
                self.source.flash(
                    filepath, self.N_FRAME_AFTER_DETECTED, self.detectmotion
                )
