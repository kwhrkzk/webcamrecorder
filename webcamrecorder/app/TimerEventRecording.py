from . import ITimerEventRecording
from . import ISendMail
from . import IDetectMotion
from ..domain.WebcameraSource import WebcameraSource
import os
from dotenv import load_dotenv
from injector import inject
from datetime import datetime, timedelta


class TimerEventRecording(ITimerEventRecording.ITimerEventRecording):
    @inject
    def __init__(
        self, sendmail: ISendMail.ISendMail, detectmotion: IDetectMotion.IDetectMotion
    ) -> None:
        load_dotenv()

        self.sendmail = sendmail
        self.detectmotion = detectmotion
        self.MAIL_SUBJECT = os.getenv("MAIL_SUBJECT") or "subject"
        self.MAIL_BODY = os.getenv("MAIL_BODY") or "body"
        self.WEBCAMERA_RECORD_MINUTES = int(os.getenv("WEBCAMERA_RECORD_MINUTES") or 10)
        self.N_FRAME_AFTER_DETECTED = int(os.getenv("N_FRAME_AFTER_DETECTED") or 500)
        self.WEBCAMERA_OUTPUTFILENAME = (
            os.getenv("WEBCAMERA_OUTPUTFILENAME") or "webcam1"
        )
        self.source = WebcameraSource(
            os.getenv("WEBCAMERA_URL"),
            int(os.getenv("N_FRAME_BEFORE_DETECTED") or "0"),
            int(os.getenv("WEBCAMERA_FPS") or "24"),
        )

    def record(self):
        start = datetime.now()
        stop = start + timedelta(minutes=self.WEBCAMERA_RECORD_MINUTES)

        while frame := self.source.createFrame():
            ret, frame = self.detectmotion.detect(frame)

            if ret:
                self.sendmail.send(frame, self.MAIL_SUBJECT, self.MAIL_BODY)

                now = format(datetime.now(), "%Y%m%d%H%M%S")
                filepath = os.path.join(
                    "store", self.WEBCAMERA_OUTPUTFILENAME + "_" + now + ".mp4"
                )
                self.source.flash(filepath, self.N_FRAME_AFTER_DETECTED)

            if datetime.now() >= stop:
                break
