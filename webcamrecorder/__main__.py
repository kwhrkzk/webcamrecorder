import webcamrecorder.domain
import webcamrecorder.app
from injector import Injector
import argparse
import os

def configure(b):
    b.bind(webcamrecorder.app.IDetectMotion.IDetectMotion, webcamrecorder.app.DetectMotion.DetectMotion)
    b.bind(webcamrecorder.app.ISendMail.ISendMail, webcamrecorder.app.SendMail.SendMail)
    b.bind(webcamrecorder.app.IContinuousRecording.IContinuousRecording, webcamrecorder.app.ContinuousRecording.ContinuousRecording)
    b.bind(webcamrecorder.app.IContinuousRecording.IContinuousRecording, webcamrecorder.app.ContinuousRecording.ContinuousRecording)
    b.bind(webcamrecorder.app.IEventRecording.IEventRecording, webcamrecorder.app.EventRecording.EventRecording)
    b.bind(webcamrecorder.app.ITimerRecording.ITimerRecording, webcamrecorder.app.TimerRecording.TimerRecording)
    b.bind(webcamrecorder.app.ITimerEventRecording.ITimerEventRecording, webcamrecorder.app.TimerEventRecording.TimerEventRecording)

injector = Injector(configure)

if not os.path.exists("store"):
    os.mkdir("store")

parser = argparse.ArgumentParser()

def timer(args):
    cr = injector.get(webcamrecorder.app.ITimerRecording.ITimerRecording)
    cr.record()

def record(ars):
    cr = injector.get(webcamrecorder.app.IContinuousRecording.IContinuousRecording)
    cr.record()

def event(args):
    er = injector.get(webcamrecorder.app.IEventRecording.IEventRecording)
    er.record()

def timer_event(args):
    er = injector.get(webcamrecorder.app.ITimerEventRecording.ITimerEventRecording)
    er.record()

def video(args):
    path = os.path.abspath(args.path)

    if os.path.isfile(path) == False:
        print("file is not exist.")
        return

    am = injector.call_with_injection(webcamrecorder.app.AnalyzeVideo.AnalyzeVideo, args=(injector.get(webcamrecorder.app.IDetectMotion.IDetectMotion), path))
    am.analyze()

sp = parser.add_subparsers()

pv = sp.add_parser("video")
pv.add_argument("--path")
pv.set_defaults(handler=video)

pt = sp.add_parser("timer")
pt.set_defaults(handler=timer)

pr = sp.add_parser("record")
pr.set_defaults(handler=record)

pe = sp.add_parser("event")
pe.set_defaults(handler=event)

pte = sp.add_parser("timerevent")
pte.set_defaults(handler=timer_event)

args = parser.parse_args()

if hasattr(args, "handler"):
    args.handler(args)
else:
    parser.print_help()
