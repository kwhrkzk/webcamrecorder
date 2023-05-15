from webcamrecorder.domain import MailSender
from webcamrecorder.domain import VideoSource 
import os
from dotenv import load_dotenv

def test_send():
    load_dotenv()

    # https://github.com/shirmung/opencv-tests/blob/master/testdata/gpu/video/768x576.avi
    path = os.path.join(os.path.abspath(os.path.curdir), "store", "testdata_gpu_video_768x576.avi")
    source = VideoSource.VideoSource(path)
    frame = source.createFrame()
    sender = MailSender.MailSender(os.environ["SMTP_SERVER_ADDRESS"], os.environ["SMTP_PORT"], os.environ["SMTP_ACCOUNT"], os.environ["SMTP_PASSWORD"])
    # sender.send(frame)

