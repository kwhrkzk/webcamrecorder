from webcamrecorder.domain import VideoSource
from injector import Injector
import webcamrecorder.app
import os
from dotenv import load_dotenv


def configure(b):
    b.bind(webcamrecorder.app.IDetectMotion.IDetectMotion, webcamrecorder.app.DetectMotion.DetectMotion)
    b.bind(webcamrecorder.app.IAnalyzeVideo.IAnalyzeVideo, webcamrecorder.app.AnalyzeVideo.AnalyzeVideo)
    b.bind(webcamrecorder.app.ISendMail.ISendMail, webcamrecorder.app.SendMail.SendMail)


def test_send():
    load_dotenv()

    injector = Injector(configure)

    # https://github.com/shirmung/opencv-tests/blob/master/testdata/gpu/video/768x576.avi
    path = os.path.join(os.path.abspath(os.path.curdir), "store", "testdata_gpu_video_768x576.avi")
    source = VideoSource.VideoSource(path)
    frame = source.createFrame()

    sendmail = injector.get(webcamrecorder.app.ISendMail.ISendMail)
    # sendmail.send(frame)

    assert True
