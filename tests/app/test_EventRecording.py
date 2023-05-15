from webcamrecorder.app import SendMail 
from webcamrecorder.app import ISendMail 
from webcamrecorder.app import IEventRecording
from webcamrecorder.app import EventRecording
from webcamrecorder.app import IContinuousRecording
from webcamrecorder.app import ContinuousRecording
from webcamrecorder.app import IDetectMotion
from webcamrecorder.app import DetectMotion
from injector import Injector

def configure(b):
    b.bind(ISendMail.ISendMail, SendMail.SendMail)
    b.bind(IDetectMotion.IDetectMotion, DetectMotion.DetectMotion)
    b.bind(IEventRecording.IEventRecording, EventRecording.EventRecording)
    b.bind(IContinuousRecording.IContinuousRecording, ContinuousRecording.ContinuousRecording)

def test_record():
    injector = Injector(configure)

    er = injector.get(IEventRecording.IEventRecording)

    er.record()
    assert True