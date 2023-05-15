from . import IEventRecording 
from . import ISendMail
from . import IDetectMotion
from ..domain.WebcameraSource import WebcameraSource 
import os
from dotenv import load_dotenv
import datetime
from injector import inject

class EventRecording(IEventRecording.IEventRecording):
    @inject
    def __init__(self, sendmail: ISendMail.ISendMail, detectmotion: IDetectMotion.IDetectMotion) -> None:
        load_dotenv()

        self.sendmail = sendmail
        self.detectmotion = detectmotion
        self.MAIL_SUBJECT = os.getenv("MAIL_SUBJECT") or "subject"
        self.MAIL_BODY = os.getenv("MAIL_BODY") or "body"
        self.N_FRAME_AFTER_DETECTED = int(os.getenv("N_FRAME_AFTER_DETECTED") or 500)
        self.WEBCAMERA_OUTPUTFILENAME = os.getenv("WEBCAMERA_OUTPUTFILENAME") or "webcam1"
        self.source = WebcameraSource(
            os.getenv("WEBCAMERA_URL"),
            int(os.getenv("N_FRAME_BEFORE_DETECTED") or "0"),
            int(os.getenv("WEBCAMERA_FPS") or "24"))

    def record(self):
        while frame := self.source.createFrame():

            ret, frame = self.detectmotion.detect(frame)

            if ret:
                self.sendmail.send(frame, self.MAIL_SUBJECT, self.MAIL_BODY)

                now = format(datetime.datetime.now(), "%Y%m%d%H%M%S")
                filepath = os.path.join("store", self.WEBCAMERA_OUTPUTFILENAME + "_" + now + ".mp4")
                self.source.flash(filepath, self.N_FRAME_AFTER_DETECTED, self.detectmotion)
