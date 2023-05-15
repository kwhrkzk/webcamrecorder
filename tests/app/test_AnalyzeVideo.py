import webcamrecorder.app
from injector import Injector
import os


def configure(b):
    b.bind(webcamrecorder.app.IDetectMotion.IDetectMotion, webcamrecorder.app.DetectMotion.DetectMotion)
    b.bind(webcamrecorder.app.IAnalyzeVideo.IAnalyzeVideo, webcamrecorder.app.AnalyzeVideo.AnalyzeVideo)


def test_analyze():
    injector = Injector(configure)

    # https://github.com/shirmung/opencv-tests/blob/master/testdata/gpu/video/768x576.avi
    path = os.path.join(os.path.abspath(os.path.curdir), "store", "testdata_gpu_video_768x576.avi")
    am = injector.call_with_injection(webcamrecorder.app.AnalyzeVideo.AnalyzeVideo, args=(injector.get(webcamrecorder.app.IDetectMotion.IDetectMotion), path))

    am.analyze()
    assert True
