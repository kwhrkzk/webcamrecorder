from webcamrecorder.domain import VideoSource


def test_VideoSource():
    source = VideoSource.VideoSource("d:\\20230421_063552_43分ころゴミ捨てられる.mp4")
    frame = source.createFrame(10300)
    ret = frame.differential_judgment(source.getBackgroundSubtractor())

    while frame := source.createFrame():
        ret = frame.differential_judgment(source.getBackgroundSubtractor())
        if ret:
            source.flash("d:\\" + str(frame.frame_position) + ".mp4", 500)
